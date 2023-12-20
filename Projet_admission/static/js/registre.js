function get_value(id) {
  let val = document.getElementById(id).value;
  return val;
}
function test() {
  let erro = document.getElementById("Error");
  let code = get_value("code_user");
  if (code.length < 7 || code.length > 11) {
    erro.innerHTML = "code invalid";
    erro.style.color = "red";
    return false;
  }
  let psswd1 = get_value("password");
  if (psswd1.length < 7 || psswd1.length > 11) {
    erro.innerHTML = "Password invalid";
    erro.style.color = "red";
    return false;
  }
  let psswd2 = get_value("passwordConfrimer");
  if (psswd2.length < 7 || psswd2.length > 11) {
    erro.innerHTML = " Confirmation Password  invalid";
    erro.style.color = "red";
    return false;
  }
  if (psswd1 != psswd2) {
    erro.innerHTML = "Passwords do not match";
    erro.style.color = "red";
    return false;
  }
}
