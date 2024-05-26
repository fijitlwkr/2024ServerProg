document.addEventListener('DOMContentLoaded', () => {
    const introductionTextarea = document.getElementById('introduction');
    const okBtn = document.getElementById('ok-btn');
    const groupsContainer = document.getElementById('groups-container');

    const nickname = 'UserNickname'; // 실제 데이터베이스에서 가져온 닉네임으로 대체
    const introduction = 'This is a brief introduction.'; // 실제 데이터베이스에서 가져온 한 줄 소개로 대체
    const joinedGroups = [
        { name: 'Group A', target: 'scheduler-1.html' },
        { name: 'Group B', target: 'scheduler-2.html' },
        { name: 'Group C', target: 'scheduler-3.html' }
    ]; // 실제 데이터베이스에서 가져온 가입된 그룹 목록으로 대체

    document.getElementById('nickname').textContent = nickname;
    introductionTextarea.value = introduction;

    joinedGroups.forEach(group => {
        const groupBlock = document.createElement('div');
        groupBlock.classList.add('group-block');
        groupBlock.textContent = group.name;
        groupBlock.setAttribute('data-target', group.target);
        groupsContainer.appendChild(groupBlock);

        groupBlock.addEventListener('click', () => {
            window.location.href = group.target;
        });
    });

    okBtn.addEventListener('click', () => {
        const updatedIntroduction = introductionTextarea.value;
        // 여기에 DB에 한 줄 소개를 업데이트하는 로직을 추가하세요.
        console.log(`Updated introduction: ${updatedIntroduction}`);
        // 업데이트 완료 후 홈 페이지로 이동
        window.location.href = 'home.html';
    });
});
