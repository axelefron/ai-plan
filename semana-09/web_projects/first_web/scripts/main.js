// 1. Referencias iniciales
const myHeading = document.querySelector("h1");
const myImage = document.querySelector("img");

// 2. Cambiador de imágenes al hacer clic
myImage.addEventListener("click", () => {
  const mySrc = myImage.getAttribute("src");
  if (mySrc === "images/foto-prueba.jpeg") { // Te recomiendo usar guiones en vez de espacios
    myImage.setAttribute("src", "images/foto-2.jpg");
  } else {
    myImage.setAttribute("src", "images/foto-prueba.jpeg");
  }
});

// 3. Referencia al botón de usuario
const myButton = document.querySelector("button");

// 4. Función de bienvenida personalizada (con validación para que no salga "null")
function setUserName() {
  const myName = prompt("Please enter your name.");
  if (!myName) {
    setUserName();
  } else {
    localStorage.setItem("name", myName);
    myHeading.textContent = `Get your credit card back, ${myName}`;
  }
}

// 5. Inicialización al cargar la página
if (!localStorage.getItem("name")) {
  setUserName();
} else {
  const storedName = localStorage.getItem("name");
  myHeading.textContent = `Get your credit card back, ${storedName}`;
}

// 6. Evento para el botón "Change user"
myButton.addEventListener("click", () => {
  setUserName();
});
