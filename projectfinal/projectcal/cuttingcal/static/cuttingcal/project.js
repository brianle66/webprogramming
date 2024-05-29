document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#edit_project').addEventListener('click', () => edit_project());
    document.querySelector('#save_project').addEventListener('click', () => save_project(true));
});

function edit_project() {
    const projectNameElement = document.querySelector("#projectName");
    const projectCodeElement = document.querySelector("#projectCode");
    const projectDateElement = document.querySelector("#projectDate");
    const projectCustomerElement = document.querySelector("#projectCustomer");
    const initialData = {
        name : projectNameElement.innerText,
        code : projectCodeElement.innerText,
        date : projectDateElement.innerText,
        customer : projectCustomerElement.innerText
    };
    document.querySelector('#save_project').style.display = 'inline-block';
    document.querySelector('#cancel_edit').style.display = 'inline-block';
    document.querySelector('#edit_project').style.display = 'none';
    projectName.innerHTML = `<input type="text" id="projectNameinput" value="${initialData.name}">`;
    projectCode.innerHTML = `<input type="text" id="projectCodeinput" value="${initialData.code}">`;
    projectDate.innerHTML = `<input type="text" id="projectDateinput" value="${initialData.date}">`;
    projectCustomer.innerHTML = `<input type="text" id="projectCustomerinput" value="${initialData.customer}">`;

    document.querySelector("#cancel_edit").addEventListener("click", () =>{
        projectName.innerHTML = initialData.name;
        projectCode.innerHTML = document.querySelector("#projectCode").value;
        projectDate.innerHTML = document.querySelector("#projectDate").value;
        projectCustomer.innerHTML = document.querySelector("#projectCustomer").value;
    })
    document.querySelector('#save_project').style.display = 'none';
    document.querySelector('#cancel_edit').style.display = 'none';
    document.querySelector('#edit_project').style.display = 'block';

}