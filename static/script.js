let fileDialog = document.getElementById("file-dialog");
let fileName = document.getElementById("file-name")

fileDialog.addEventListener("change", ()=>{
    let file = document.querySelector("input[type=file]").files[0];

    fileName.value = file.name;
})