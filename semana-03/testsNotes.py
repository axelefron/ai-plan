# it is used to check code rather than believe it works before trying corner cases
# can be used to evaluate previous code on other files by importing them
# unit test is for testing with manual code using assertions, but is long and not really used in an extended code

# assert -->  keyword to assert that something is true, and if its nothing happens, 
# but if you assert something that is false, you see an error on screen

# AssertionError --> error in the assertion statemnt
# use try except to catch the error

# pytest --> third party program that can be installed and is autmated to test on my code
# pip3 install pytest para bajar y usar pytest

# se separan los test en el file de lo que se quiere testear (importado) en diferentes funciones
# para que corran todos los asserts y detecte todos los errores en vez de frenar al primer error
# dice si es correcto o no el asssertion de los que yo defini, no significa que todo el codigo funciona bien, solo las pruebas

# importante que en las funciones use return mas que print, por que print no guarda nada y cuando hago el test se rompe por que no hay valor para testear
# " == " es para buscar si hay un returned value

# packages are modeules organized inside a folder
# __init__ --> for python to detect that is a package