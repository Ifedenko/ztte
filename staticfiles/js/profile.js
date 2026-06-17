document.addEventListener('DOMContentLoaded', function() {
    // Вкладки
    const tabs = document.querySelectorAll('.tab-btn');
    const contents = document.querySelectorAll('.tab-content');
    tabs.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabId = btn.dataset.tab;
            tabs.forEach(b => b.classList.remove('active'));
            contents.forEach(c => c.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById(`${tabId}-tab`).classList.add('active');
        });
    });

    // Показ/скрытие полей года и группы
    const roleSelect = document.getElementById('id_role');
    const yearGroup = document.getElementById('year-group');
    const yearLabel = document.getElementById('year-label');
    const groupGroup = document.getElementById('group-group');

    function toggleFields() {
        const role = roleSelect.value;
        if (role === 'student') {
            yearGroup.style.display = 'block';
            yearLabel.textContent = 'Год поступления';
            groupGroup.style.display = 'block';
        } else if (role === 'graduate') {
            yearGroup.style.display = 'block';
            yearLabel.textContent = 'Год выпуска';
            groupGroup.style.display = 'block';
        } else {
            yearGroup.style.display = 'none';
            groupGroup.style.display = 'none';
        }
    }

    roleSelect.addEventListener('change', toggleFields);
    toggleFields();

    // При отправке очищаем скрытые поля
    const form = document.querySelector('.profile-form');
    form.addEventListener('submit', function() {
        const role = roleSelect.value;
        if (role !== 'student' && role !== 'graduate') {
            document.getElementById('id_year').value = '';
            document.getElementById('id_group_name').value = '';
        }
    });
});