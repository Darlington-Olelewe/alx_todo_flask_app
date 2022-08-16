
document.getElementById('form').onsubmit = (e) => {
    e.preventDefault();
    const method = 'POST';
    const body = JSON.stringify({'description': document.getElementById('description').value });
    const headers = {'Content-Type': 'application/json'};
    
    fetch('/todos/create', {
        method,
        body,
        headers 
    }).then((response) => response.json())
    .then((response) => {
    const liItem = document.createElement('LI');
    liItem.innerHTML = response['description']
    document.getElementById('todos').appendChild(liItem)})
    .catch((error)=>{
        console.log("Error occured");
        console.log(error);
    })
    
}

const checkboxes = document.querySelectorAll('.check-class');

for(let i = 0; i < checkboxes.length; i++){
    const checkbox = checkboxes[i];
    checkbox.onChange = (e)=>{
        console.log('evt', e)
    }
}