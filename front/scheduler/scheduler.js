document.addEventListener('DOMContentLoaded', () => {
    const memberListBtn = document.getElementById('member-list-btn');
    const cancelBtn = document.getElementById('cancel-btn');
    const leaveBtn = document.getElementById('leave-btn');

    memberListBtn.addEventListener('click', () => {
        window.location.href = 'member-list.html'; // 회원 목록 조회 페이지로 이동
    });

    cancelBtn.addEventListener('click', () => {
        window.location.href = 'home.html'; // 홈 페이지로 이동
    });

    leaveBtn.addEventListener('click', () => {
        // 그룹 탈퇴 로직 추가
        // 서버에 요청을 보내고 응답을 처리
        alert('그룹을 탈퇴했습니다.');
        window.location.href = 'home.html'; // 홈 페이지로 이동
    });

    // 여기에 체크리스트 항목을 동적으로 추가하는 로직을 추가하세요.
    // 예를 들어, 서버에서 데이터를 받아와서 추가합니다.
});
