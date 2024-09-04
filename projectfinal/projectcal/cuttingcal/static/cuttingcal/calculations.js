document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM fully loaded and parsed");

    const projectNameInput = document.getElementById('projectName');
    const projectmessageElement = document.getElementById('projectNameMessage');

    // Function to check project name availability
    function checkProjectName() {
        const projectName = projectNameInput.value.trim();

        if (projectName) {
            fetch(`/check_project_name/?name=${encodeURIComponent(projectName)}`)
                .then(response => response.json())
                .then(data => {
                    if (data.available) {
                        projectmessageElement.textContent = "This project is available";
                        projectmessageElement.style.color = "green";
                    } else {
                        projectmessageElement.textContent = "This project name is already taken";
                        projectmessageElement.style.color = "red";
                    }
                })
                .catch(error => console.error('Error:', error));
        } else {
            projectmessageElement.textContent = ""; // Clear the message if input is empty
        }
    }

    // Event listener for when the input loses focus
    projectNameInput.addEventListener('blur', checkProjectName);

    const customerNameInput = document.getElementById('customerName');
    const customerMessageElement = document.getElementById('customerNameMessage');

    function checkCustomerName() {
        const customerName = customerNameInput.value.trim();

        if (customerName) {
            fetch(`/check_customer_name/?name=${encodeURIComponent(customerName)}`)
                .then(response => response.json())
                .then(data => {
                    if (data.available) {
                        customerMessageElement.textContent = "This customer is available";
                        customerMessageElement.style.color = "green";
                    } else {
                        customerMessageElement.textContent = "This customer name is already taken";
                        customerMessageElement.style.color = "red";
                    }
                })
                .catch(error => console.error('Error:', error));
        } else {
            customerMessageElement.textContent = ""; // Clear the message if input is empty
        }
    }

    customerNameInput.addEventListener('input', checkCustomerName); // Trigger on every input change
});
