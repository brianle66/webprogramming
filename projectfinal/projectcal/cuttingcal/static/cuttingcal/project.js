document.addEventListener('DOMContentLoaded', function() {
    const projectNameElement = document.querySelector("#projectName");
    const projectCodeElement = document.querySelector("#projectCode");
    const projectDateElement = document.querySelector("#projectDate");
    const projectCustomerElement = document.querySelector("#projectCustomer");

    const initialData = {
        name: projectNameElement.innerText.split(': ')[1],
        code: projectCodeElement.innerText.split(': ')[1], // Extract the actual code value
        date: projectDateElement.innerText.split(': ')[1], // Extract the actual date value
        customer: projectCustomerElement.innerText.split(': ')[1] // Extract the actual customer value
    };

    document.querySelector('#edit_project').addEventListener('click', edit_project);
    document.querySelector('#cancel_edit').addEventListener('click', cancel_edit);
    document.querySelector('#save_project').addEventListener('click', save_project);
    document.querySelectorAll('#edit_order').forEach(button => {
        button.addEventListener('click', edit_order);
    });
    
    function edit_order(event) {
        const button = event.target;
        const projectCode = button.dataset.projectCode;
        const orderId = button.dataset.orderId;
        const url = `/project/${projectCode}/${orderId}/`;
    
        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                return response.json();
            })
            .then(data => {
                if (data.error) {
                    throw new Error(data.error);
                }
                displayEditForm(data);
            })
            .catch(error => console.error('Error fetching order data:', error));
    }
    
    function displayEditForm(data) {
        const form = `
            <form id="editOrderForm">
                <input type="hidden" name="order_id" value="${data.id}">
                <div class="mb-3">
                    <label for="date" class="form-label">Date</label>
                    <input type="date" class="form-control" id="date" name="date" value="${data.date.split('T')[0]}">
                </div>
                <div class="mb-3">
                    <label for="style" class="form-label">Style</label>
                    <input type="text" class="form-control" id="style" name="style" value="${data.style}">
                </div>
                <button type="submit" class="btn btn-primary">Save</button>
            </form>
        `;
    
        const modalBody = document.getElementById('modalBody');
        modalBody.innerHTML = form;
    
        const modal = new bootstrap.Modal(document.getElementById('editOrderModal'));
        modal.show();
    
        document.getElementById('editOrderForm').addEventListener('submit', save_project);
    }

    function save_order(event) {
        event.preventDefault();
        const formData = new FormData(event.target);
        const url = '/update_order/';
    
        fetch(url, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    console.error('Error updating order:', data.error);
                }
            })
            .catch(error => console.error('Error:', error));
    }

    function edit_project() {
        document.querySelector('#save_project').style.display = 'inline-block';
        document.querySelector('#cancel_edit').style.display = 'inline-block';
        document.querySelector('#edit_project').style.display = 'none';


        projectNameElement.innerHTML = `<input type="text" id="projectNameInput" value="${initialData.name}">`;
        projectCodeElement.innerHTML = `<input type="text" id="projectCodeInput" value="${initialData.code}">`;
        projectDateElement.innerHTML = `<input type="date" id="projectDateInput" value="${initialData.date}">`;
        projectCustomerElement.innerHTML = `<input type="text" id="projectCustomerInput" value="${initialData.customer}">`;
    }

    function cancel_edit() {
        projectNameElement.innerHTML = `Project: ${initialData.name}`;
        projectCodeElement.innerHTML = `Code: ${initialData.code}`; // Restore the original format
        projectDateElement.innerHTML = `Date: ${initialData.date}`; // Restore the original format
        projectCustomerElement.innerHTML = `Customer: ${initialData.customer}`; // Restore the original format

        document.querySelector('#save_project').style.display = 'none';
        document.querySelector('#cancel_edit').style.display = 'none';
        document.querySelector('#edit_project').style.display = 'inline-block';
    }

    function save_project() {
        const projectNameInput = document.querySelector("#projectNameInput").value;
        const projectCodeInput = document.querySelector("#projectCodeInput").value;
        const projectDateInput = document.querySelector("#projectDateInput").value;
        const projectCustomerInput = document.querySelector("#projectCustomerInput").value;

        const projectDate = new Date(projectDateInput).toISOString();

        fetch('/update_project/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                name: projectNameInput,
                code: projectCodeInput,
                date: projectDate,
                customer: projectCustomerInput
            })
        }).then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        }).then(data => {
            if (data.success) {
                projectNameElement.innerText = `Project: ${projectNameInput}`;
                projectCodeElement.innerText = `Code: ${projectCodeInput}`;
                projectDateElement.innerText = `Date: ${projectDateInput}`;
                projectCustomerElement.innerText = `Customer: ${projectCustomerInput}`;

                document.querySelector('#save_project').style.display = 'none';
                document.querySelector('#cancel_edit').style.display = 'none';
                document.querySelector('#edit_project').style.display = 'inline-block';
            } else {
                console.error('Failed to update project:', data);
                alert('Failed to update project');
            }
        }).catch(error => {
            console.error('Error:', error);
            alert('Failed to update project');
        });
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
