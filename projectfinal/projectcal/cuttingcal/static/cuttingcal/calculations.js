document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM fully loaded and parsed");

    const projectNameInput = document.getElementById('projectName');
    const projectmessageElement = document.getElementById('projectNameMessage');
    const customerNameInput = document.getElementById('customerName');
    const customerMessageElement = document.getElementById('customerNameMessage');
    const saveProjectCheckbox = document.getElementById('saveProject');
    const clearButton = document.getElementById('clearButton');
    const orderInfoSection = document.querySelector('.orderinfo');

    // Function to check fabric component of the current selected Style
    function fetchLatestOrderId() {
        if (!projectNameInput) {
          console.error('Element with id "projectName" not found!');
          return;
        }
  
        const projectName = projectNameInput.value.trim();
        
        if (!projectName) {
          // Clear the placeholder if project name is empty
          document.getElementById('orderID').placeholder = '';
          console.log('Project name is empty, cannot fetch order ID.');
          return;
        }
  
        // Make the AJAX request to fetch the latest order ID
        fetch(`/get_order_id/?name=${encodeURIComponent(projectName)}`)
        .then(response => response.json())
        .then(data => {
            if (data.latest_order_id) {
            // Set the orderID input's placeholder to the fetched order ID
            document.getElementById('orderID').placeholder = data.latest_order_id;
            } else if (data.error) {
            alert(data.error);  // Handle the error returned from the server
            document.getElementById('orderID').placeholder = 'N/A';  // Reset placeholder in case of error
            }
        })
        .catch(error => {
            console.error('Error fetching the latest order ID:', error);
            document.getElementById('orderID').placeholder = 'N/A';  // Reset placeholder on failure
        });
      }
    

    // Function to disable orderinfo 
    function toggleOrderInfo() {
        if (projectNameInput.value.trim() && customerNameInput.value.trim()) {
            orderInfoSection.querySelectorAll('input, select').forEach(function(input) {
                input.disabled = false;
            });
        } else {
            orderInfoSection.querySelectorAll('input, select').forEach(function(input) {
                input.disabled = true;
            });
        }
    }

    //Check everytime input changing and update the block status by using toggleOrderInfo
    projectNameInput.addEventListener('input', toggleOrderInfo);
    customerNameInput.addEventListener('input', toggleOrderInfo);

    toggleOrderInfo(); // Initial check

    //Create or update project
    function createOrUpdateProject() {
        const projectName = projectNameInput.value.trim();
        const customerName = customerNameInput.value.trim();
        const saveProject = saveProjectCheckbox.checked;

        if (saveProject && projectName && customerName) {
            const data = {
                project_name: projectName,
                customer_name: customerName
            };

            fetch('/create_or_update_project/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify(data)
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'created') {
                        alert('Project and customer created successfully!');
                    } else if (data.status === 'updated') {
                        alert('Project updated with new order.');
                    }
                })
                .catch(error => console.error('Error:', error));
        }
    }

    document.querySelector('form').addEventListener('submit', function (e) {
        e.preventDefault();
        createOrUpdateProject();
    });

    // Clear button event listener
    clearButton.addEventListener('click', function(event) {
        event.preventDefault(); // Prevent form submission

        // Clear the input fields
        projectNameInput.value = '';
        customerNameInput.value = '';
        
        // Clear the validation messages
        projectmessageElement.textContent = '';
        customerMessageElement.textContent = '';

        // Clear save checkbox
        saveProjectCheckbox.checked = false;

        toggleOrderInfo();
    });

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


    // Fuction to check customer nam available
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


    //When input lost focus, execute the function to the availability 
    projectNameInput.addEventListener('blur', checkProjectName);
    projectNameInput.addEventListener('blur', fetchLatestOrderId);
    customerNameInput.addEventListener('blur', checkCustomerName);
});
