function deleteApply(applyId, applyName) {
    if (confirm('Удалить отклик "' + applyName + '"?')) {
        fetch('/dashboard/delete/' + applyId, {
            method: 'DELETE'
        })
        .then(response => {
            if (response.ok) {
                // Удаляем элемент из DOM
                const element = document.getElementById('apply-' + applyId);
                if (element) {
                    element.remove();
                }
                // Показываем сообщение об успехе
                showMessage('Отклик успешно удален!', 'success');
            } else {
                showMessage('Ошибка при удалении отклика', 'error');
            }
        })
        .catch(error => {
            showMessage('Ошибка при удалении отклика', 'error');
        });
    }
}

function showMessage(message, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = type;
    messageDiv.textContent = message;
    messageDiv.style.position = 'fixed';
    messageDiv.style.top = '20px';
    messageDiv.style.right = '20px';
    messageDiv.style.zIndex = '1000';
    messageDiv.style.padding = '15px';
    messageDiv.style.borderRadius = '8px';
    messageDiv.style.color = type === 'success' ? '#155724' : '#721c24';
    messageDiv.style.backgroundColor = type === 'success' ? '#d4edda' : '#f8d7da';
    messageDiv.style.border = '1px solid ' + (type === 'success' ? '#c3e6cb' : '#f5c6cb');
    
    document.body.appendChild(messageDiv);
    
    setTimeout(() => {
        messageDiv.remove();
    }, 3000);
} 