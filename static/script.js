let fileDialog = document.getElementById("file-dialog");
let fileName = document.getElementById("file-name")

// Gather error text
tipError = document.getElementById('tip-error')
fileError = document.getElementById('file-error')

fileDialog.addEventListener("change", ()=>{
    let file = document.querySelector("input[type=file]").files[0];
    fileError.innerHTML = ''

    // fileName.value = file.name

    //Validate selected file
    fileType = file.name.substr(file.name.lastIndexOf('.'))
    if(fileType != '.pdf') {
        fileError.innerHTML = 'Only PDF files are supported'
    } else if(file.size > 50000) {
        fileError.innerHTML = 'File too large'
    } else {
        fileName.value = file.name
    }
})


function validateForm() {

    // Set submit flag
    flag = false

    tipError.innerHTML = ''
    fileError.innerHTML = ''

    // Validate tip amount
    tipField = document.getElementById('tip-amount')
    tipStr = tipField.value

    // Check if input field is empty
    if(tipStr == '') {
        tipError.innerHTML = 'Field can not be empty'
        flag = false
    }  else {
        // If it's not empty make sure it contains only numbers
        isnum = /^\d+$/.test(tipStr)
        if(!isnum) {
            tipError.innerHTML = 'The field should contain only numbers'
            flag = false
        }
    }



    // Validate file
    fileField = document.getElementById('file-name')
    fileStr = fileField.value

    // Check if a file has been set in the input field
    if(fileStr == '') {
        fileError.innerHTML = 'A file must be selected'
        flag = false
    }


    return flag
}