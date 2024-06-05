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
