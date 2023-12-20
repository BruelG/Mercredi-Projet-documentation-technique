// affiche dropdowPropos
function showDropdown_Admiss() {
  document.getElementById("admissionDropdown").style.display = "block";
}
// cache dropdownPropos
function hideDropdown_Admiss() {
  document.getElementById("admissionDropdown").style.display = "none";
}

// affiche dropdownProgramme
function showDropdown_Programme() {
  document.getElementById("programmeDropdown").style.display = "block";
}
// cache dropdownProgramme
function hideDropdown_Programme() {
  document.getElementById("programmeDropdown").style.display = "none";
}

// affiche dropdowPropos
function showDropdown_Propos() {
  document.getElementById("proposDropdown").style.display = "block";
}
// cache dropdownPropos
function hideDropdow_Propos() {
  document.getElementById("proposDropdown").style.display = "none";
}

// affiche dropdowContact
function showDropdown_Contact() {
  document.getElementById("contactDropdow").style.display = "block";
}
// cache dropdownContact
function hideDropdow_Contact() {
  document.getElementById("contactDropdow").style.display = "none";
}

// chat
// Fonction d'ouverture du chat
function openChat() {
  // Ajoutez ici la logique pour ouvrir le chat
  // Par exemple, vous pouvez afficher une boîte de dialogue ou un formulaire de chat
  // Assurez-vous d'ajouter la logique complète du chatbot en fonction de vos besoins spécifiques
  alert("Le chat s'ouvre !");
}

// Vous pouvez également ajouter une fonction pour fermer le chat si nécessaire
function closeChat() {
  // Ajoutez ici la logique pour fermer le chat
  alert("Le chat se ferme !");
}
// sippiner faire demande
function showSpinner(event) {
  event.preventDefault(); // Empêcher le comportement par défaut du lien
  const link = event.target; // Lien cliqué

  // Remplacer le texte par le spinner
  link.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Attendez...';

  // Rétablir le texte après 10 secondes
  setTimeout(function () {
    link.innerHTML = "Faire une demande";
  }, 10000); // 10 secondes en millisecondes
}

// Ajouter un gestionnaire d'événement au clic du lien
const admissionLink = document.querySelector(
  "a[href=\"{% url 'admission' %}\"]"
);
admissionLink.addEventListener("click", showSpinner);
