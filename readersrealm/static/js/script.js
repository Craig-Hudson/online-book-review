// Function to send emails to myself from users, and then display a thankyou message in a modal
function sendMail(contactForm) {
    emailjs.send("service_z478yla", "template_i89e0w9", {
        "from_name": contactForm.name.value,
        "from_email": contactForm.email.value,
        "message": contactForm.message.value
    })
    .then(
        function(response) {
            console.log("SUCCESS", response);
            $('#successModal').modal('show');  // Show the success modal
        },
        function(error) {
            console.log("FAILED", error);
        }
    );
    return false;  // To block from loading a new page
}