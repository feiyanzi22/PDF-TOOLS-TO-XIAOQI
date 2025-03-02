function handleOption(option) {
    const resultDiv = document.getElementById('result');
    switch(option) {
        case 2: // PDF 拆分
            selectFileAndProcess('pdf_split', resultDiv);
            break;
        // 其他选项的处理逻辑...
        default:
            resultDiv.innerHTML = '无效选项，请重试';
    }
}

function selectFileAndProcess(action, resultDiv) {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.pdf';
    input.onchange = function(event) {
        const file = event.target.files[0];
        if (file) {
            const formData = new FormData();
            formData.append('file', file);
            formData.append('action', action);
            
            fetch('/process', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // 使用模板字符串来避免HTML标签直接出现在JavaScript中
                    resultDiv.innerHTML = `处理完成，文件保存于：<a href="${data.filePath}" download>下载拆分后的PDF</a>`;
                } else {
                    resultDiv.innerHTML = '处理失败：' + data.error;
                }
            })
            .catch(error => {
                resultDiv.innerHTML = '发生错误：' + error.message;
            });
        }
    };
    input.click();
}
