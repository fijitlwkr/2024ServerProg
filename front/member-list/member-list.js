document.addEventListener('DOMContentLoaded', () => {
    const groupNameElement = document.getElementById('group-name');
    const memberList = document.getElementById('member-list');
    const backBtn = document.getElementById('back-btn');

    // 예시 데이터, 실제로는 서버에서 데이터 불러와야 함
    const groupName = "Example Group";  // 실제로는 서버에서 받아와야 함
    const members = [
        { nickname: 'User1', introduction: 'Hello, I am User1.' },
        { nickname: 'User2', introduction: 'Hello, I am User2.' },
        { nickname: 'User3', introduction: 'Hello, I am User3.' },
    ];

    // 서버에서 그룹명과 회원 목록을 불러오는 함수
    function fetchGroupData() {
        // 여기에 실제 서버와 통신하는 코드 추가 (예: Fetch API 또는 AJAX)
        // 예시:
        /*
        fetch('/api/group_data')  // 실제 서버의 URL로 변경
            .then(response => response.json())
            .then(data => {
                groupNameElement.textContent = data.groupName;
                populateMemberList(data.members);
            })
            .catch(error => console.error('Error:', error));
        */
        
        // 예시 데이터로 그룹명과 리스트를 채우는 코드
        groupNameElement.textContent = groupName;
        populateMemberList(members);
    }

    // 회원 목록을 HTML에 추가하는 함수
    function populateMemberList(members) {
        memberList.innerHTML = '';  // 기존 목록 초기화
        members.forEach(member => {
            const li = document.createElement('li');
            li.innerHTML = `<strong>${member.nickname}</strong><br>${member.introduction}`;
            memberList.appendChild(li);
        });
    }

    backBtn.addEventListener('click', () => {
        window.location.href = 'scheduler.html';  // 스케줄러 페이지로 이동
    });

    // 페이지 로드 시 그룹명과 회원 목록을 불러옴
    fetchGroupData();
});
