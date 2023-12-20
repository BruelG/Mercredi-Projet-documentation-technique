// etap_4.js

// Fonction pour afficher le formulaire Visa
function showVisaForm() {
  //   document.getElementById("visa_form").style.display = "block";
  alert("Bonjour");
}

// Fonction pour le paiement Visa (remplacez par votre propre logique de paiement)
function processVisaPayment() {
  alert(
    "Traitement du paiement Visa... (Remplacez ceci par votre propre logique de paiement)"
  );
}

// Écouteur d'événement pour le clic sur l'icône Visa
document.getElementById("visa_link").addEventListener("click", showVisaForm);

// Écouteur d'événement pour le clic sur le bouton de paiement Visa
document
  .getElementById("visa-payment-button")
  .addEventListener("click", processVisaPayment);
