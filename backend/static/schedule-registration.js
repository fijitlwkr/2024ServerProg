//document.addEventListener('DOMContentLoaded', () => {
//    const form = document.getElementById('schedule-form');
//    const addTaskBtn = document.getElementById('add-task-btn');
//    const createBtn = document.getElementById('create-btn');
//
//    addTaskBtn.addEventListener('click', () => {
//        const tasksContainer = document.getElementById('tasks-container');
//        const taskDiv = document.createElement('div');
//        taskDiv.classList.add('task');
//        taskDiv.innerHTML = `
//            <input type="text" class="task-input" name="task[]" required>
//            <button type="button" class="delete-task-btn">Delete</button>
//        `;
//        tasksContainer.appendChild(taskDiv);
//    });
//
//    form.addEventListener('click', (e) => {
//        if (e.target.classList.contains('delete-task-btn')) {
//            e.target.parentElement.remove();
//        }
//    });
//
//    form.addEventListener('submit', (e) => {
//        e.preventDefault();
//        // 여기에 스케줄을 데이터베이스에 저장하는 로직을 추가하세요.
//        // 저장 후에는 홈 페이지로 이동하거나 다른 작업을 수행하세요.
//        alert('Schedule created successfully!');
//        window.location.href = 'home.html'; // 예시: 홈 페이지로 이동
//    });
//});
