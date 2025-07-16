from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from database import get_db
import models

router = APIRouter()


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, user_id: int = None):
    """Дашборд для просмотра откликов пользователя"""
    
    # Формируем HTML контент
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Applyr Dashboard</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }}
            .container {{
                background: white;
                border-radius: 12px;
                padding: 30px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            h1 {{
                color: #333;
                margin-bottom: 30px;
                text-align: center;
            }}
            .search-form {{
                margin-bottom: 30px;
                text-align: center;
            }}
            input[type="number"] {{
                padding: 12px 16px;
                border: 2px solid #ddd;
                border-radius: 8px;
                font-size: 16px;
                width: 200px;
                margin-right: 10px;
            }}
            button {{
                padding: 12px 24px;
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                cursor: pointer;
                transition: background-color 0.2s;
            }}
            button:hover {{
                background-color: #0056b3;
            }}
            .applies-list {{
                margin-top: 30px;
            }}
            .apply-item {{
                background: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 8px;
                padding: 20px;
                margin-bottom: 15px;
                transition: transform 0.2s;
            }}
            .apply-item:hover {{
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }}
            .apply-title {{
                font-size: 18px;
                font-weight: 600;
                color: #333;
                margin-bottom: 10px;
            }}
            .apply-meta {{
                color: #666;
                font-size: 14px;
                margin-bottom: 10px;
            }}
            .apply-link {{
                color: #007bff;
                text-decoration: none;
                font-weight: 500;
            }}
            .apply-link:hover {{
                text-decoration: underline;
            }}
            .apply-actions {{
                margin-top: 15px;
                display: flex;
                gap: 10px;
            }}
            .delete-btn {{
                padding: 8px 16px;
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                cursor: pointer;
                transition: background-color 0.2s;
            }}
            .delete-btn:hover {{
                background-color: #c82333;
            }}
            .no-applies {{
                text-align: center;
                color: #666;
                font-style: italic;
                padding: 40px;
            }}
            .error {{
                background: #f8d7da;
                color: #721c24;
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 20px;
            }}
            .success {{
                background: #d4edda;
                color: #155724;
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 20px;
            }}
        </style>
        <script>
            function deleteApply(applyId, applyName) {{
                if (confirm('Удалить отклик "' + applyName + '"?')) {{
                    fetch('/dashboard/delete/' + applyId, {{
                        method: 'DELETE'
                    }})
                    .then(response => {{
                        if (response.ok) {{
                            // Удаляем элемент из DOM
                            const element = document.getElementById('apply-' + applyId);
                            if (element) {{
                                element.remove();
                            }}
                            // Показываем сообщение об успехе
                            showMessage('Отклик успешно удален!', 'success');
                        }} else {{
                            showMessage('Ошибка при удалении отклика', 'error');
                        }}
                    }})
                    .catch(error => {{
                        showMessage('Ошибка при удалении отклика', 'error');
                    }});
                }}
            }}
            
            function showMessage(message, type) {{
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
                
                setTimeout(() => {{
                    messageDiv.remove();
                }}, 3000);
            }}
        </script>
    </head>
    <body>
        <div class="container">
            <h1>📋 Applyr Dashboard</h1>
            
            <div class="search-form">
                <form method="GET">
                    <input type="number" name="user_id" placeholder="Введите ID пользователя" 
                           value="{user_id if user_id else ''}" required>
                    <button type="submit">Показать отклики</button>
                </form>
            </div>
    """
    
    if user_id:
        try:
            # Получаем отклики пользователя
            db = next(get_db())
            applies = db.query(models.Apply).filter(models.Apply.user_id == user_id).order_by(models.Apply.created_at.desc()).all()
            
            if applies:
                html_content += '<div class="applies-list">'
                for apply in applies:
                    # Экранируем название для JavaScript
                    safe_name = apply.name.replace("'", "\\'").replace('"', '\\"')
                    html_content += f"""
                    <div class="apply-item" id="apply-{apply.id}">
                        <div class="apply-title">{apply.name}</div>
                        <div class="apply-meta">
                            📅 Создан: {apply.created_at.strftime('%d.%m.%Y %H:%M')}
                        </div>
                        <div class="apply-meta">
                            🔗 <a href="{apply.link}" class="apply-link" target="_blank">Перейти к вакансии</a>
                        </div>
                        <div class="apply-actions">
                            <button class="delete-btn" onclick="deleteApply('{apply.id}', '{safe_name}')">
                                🗑️ Удалить
                            </button>
                        </div>
                    </div>
                    """
                html_content += '</div>'
            else:
                html_content += '<div class="no-applies">У пользователя пока нет откликов</div>'
                
        except Exception as e:
            html_content += f'<div class="error">Ошибка при получении данных: {str(e)}</div>'
    
    html_content += """
        </div>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)


@router.delete("/dashboard/delete/{apply_id}")
async def delete_apply(apply_id: str):
    """Удаляет отклик по ID"""
    try:
        db = next(get_db())
        apply = db.query(models.Apply).filter(models.Apply.id == apply_id).first()
        
        if not apply:
            raise HTTPException(status_code=404, detail="Отклик не найден")
        
        db.delete(apply)
        db.commit()
        
        return {"message": "Отклик успешно удален"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении: {str(e)}") 