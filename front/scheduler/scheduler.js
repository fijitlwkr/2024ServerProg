document.addEventListener('DOMContentLoaded', () => {
    const groupName = 'Example Group'; // 실제 데이터베이스에서 가져온 그룹 이름으로 대체
    const groupInfo = 'This is some information about the example group.'; // 실제 데이터베이스에서 가져온 그룹 정보로 대체
    const checklistItems = [
        { text: 'Check Item 1', completed: false },
        { text: 'Check Item 2', completed: true },
        { text: 'Check Item 3', completed: false }
    ]; // 실제 데이터베이스에서 가져온 체크리스트 항목으로 대체

    document.getElementById('group-name').textContent = `Group Name: ${groupName}`;
    document.getElementById('group-info').textContent = `Group Info: ${groupInfo}`;

    const checklist = document.getElementById('checklist');
    checklistItems.forEach(item => {
        const listItem = document.createElement('li');
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.checked = item.completed;
        const label = document.createElement('label');
        label.textContent = item.text;
        listItem.appendChild(checkbox);
        listItem.appendChild(label);
        checklist.appendChild(listItem);

        checkbox.addEventListener('change', () => {
            item.completed = checkbox.checked;
            // 완료 여부를 데이터베이스에 저장하는 로직을 여기에 추가하세요.
        });
    });

    document.getElementById('cancel-btn').addEventListener('click', () => {
        window.location.href = 'profile.html'; // 프로필 페이지로 이동
    });

    document.getElementById('leave-btn').addEventListener('click', () => {
        if (confirm('그룹을 탈퇴하시겠습니까?')) {
            // 그룹 탈퇴 로직을 여기에 추가하세요.
            alert('그룹을 탈퇴했습니다.');
            window.location.href = 'profile.html'; // 프로필 페이지로 이동
        }
    });
});
