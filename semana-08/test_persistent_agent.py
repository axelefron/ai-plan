import types
import pytest
import persistent_agent as agent


@pytest.fixture(autouse=True)
def no_sleep(monkeypatch):
    monkeypatch.setattr(agent.time, "sleep", lambda s: None)


def test_retry_recovers_after_transient_errors(monkeypatch):
    calls = {"n": 0}

    def fake_execute(name, args):
        calls["n"] += 1
        if calls["n"] <= 2:
            raise agent.TransientToolError("timeout")
        return "ok"

    monkeypatch.setattr(agent, "execute_tool", fake_execute)
    assert agent.execute_with_retries("search_in_csv", {}) == "ok"
    assert calls["n"] == 3


def test_permanent_error_is_not_retried(monkeypatch):
    calls = {"n": 0}

    def fake_execute(name, args):
        calls["n"] += 1
        raise ValueError("bad input")

    monkeypatch.setattr(agent, "execute_tool", fake_execute)
    with pytest.raises(ValueError):
        agent.execute_with_retries("search_in_csv", {})
    assert calls["n"] == 1


def test_retries_run_out(monkeypatch):
    calls = {"n": 0}

    def fake_execute(name, args):
        calls["n"] += 1
        raise agent.TransientToolError("timeout")

    monkeypatch.setattr(agent, "execute_tool", fake_execute)
    with pytest.raises(agent.TransientToolError):
        agent.execute_with_retries("search_in_csv", {})
    assert calls["n"] == agent.MAX_RETRIES + 1


def test_running_state_is_found_and_done_is_not(monkeypatch, tmp_path):
    monkeypatch.setattr(agent, "STATE_DIR", tmp_path)
    assert agent.load_pending() is None

    state = agent.new_state("hola")
    state["status"] = "running"
    agent.save_state(state)
    assert agent.load_pending() is not None

    state["status"] = "done"
    agent.save_state(state)
    assert agent.load_pending() is None


@pytest.mark.parametrize("answer,expected", [("y", True), (" Y ", True), ("n", False), ("", False)])
def test_approval_only_accepts_y(monkeypatch, answer, expected):
    monkeypatch.setattr("builtins.input", lambda prompt="": answer)
    tool_use = types.SimpleNamespace(name="save_report", input={"content": "x"})
    assert agent.ask_approval(tool_use) is expected
