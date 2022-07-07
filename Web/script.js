function setPath(path) {
    document.getElementById('file-path').value = path
}

document.getElementById('file-dialog').addEventListener('click', event => {
    pywebview.api.openDialog().then(setPath)
})



document.getElementById('generate-report').addEventListener('click', event => {
    path = document.getElementById('file-path').value

    totalTipsStr = document.getElementById('tip-amount').value
    if(typeof totalTipsStr == 'string') {
        num = Number(totalTipsStr)
        if(Number.isInteger(num) && num > 0) {
            window.pywebview.api.createNewReport(path, num)
        }
    }
})