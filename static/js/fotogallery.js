document.addEventListener('DOMContentLoaded', function() {
    // ---- Фильтры из URL ----
    const urlParams = new URLSearchParams(window.location.search);
    const yearParam = urlParams.get('year');
    const monthParam = urlParams.get('month');
    const yearSelect = document.getElementById('yearSelect');
    const monthSelect = document.getElementById('monthSelect');

    if (yearSelect && yearParam) {
        yearSelect.value = yearParam;
        if (monthSelect) monthSelect.style.display = 'inline-block';
    }
    if (monthSelect && monthParam) monthSelect.value = monthParam;
    if (yearSelect && yearSelect.value && monthSelect) monthSelect.style.display = 'inline-block';

    // ---- Клики по кнопкам фильтров ----
    const filterBtns = document.querySelectorAll('.filter-btn');
    filterBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            filterBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');

            let url = window.location.pathname + '?';
            const filterVal = this.dataset.filter;
            const yearVal = yearSelect ? yearSelect.value : '';
            const monthVal = monthSelect ? monthSelect.value : '';

            if (filterVal) url += `filter=${filterVal}&`;
            if (yearVal) url += `year=${yearVal}&`;
            if (monthVal) url += `month=${monthVal}&`;
            url = url.replace(/&$/, '');
            window.location.href = url;
        });
    });

    // ---- Год ----
    if (yearSelect) {
        yearSelect.addEventListener('change', function() {
            filterBtns.forEach(b => b.classList.remove('active'));
            let url = window.location.pathname + '?';
            if (this.value) url += `year=${this.value}&`;
            if (monthSelect && monthSelect.value) url += `month=${monthSelect.value}&`;
            url = url.replace(/&$/, '');
            window.location.href = url;
        });
    }

    // ---- Месяц ----
    if (monthSelect) {
        monthSelect.addEventListener('change', function() {
            filterBtns.forEach(b => b.classList.remove('active'));
            let url = window.location.pathname + '?';
            if (yearSelect && yearSelect.value) url += `year=${yearSelect.value}&`;
            if (this.value) url += `month=${this.value}&`;
            url = url.replace(/&$/, '');
            window.location.href = url;
        });
    }

    // ---- Модальное окно ----
    const modal = document.getElementById('modal');
    const modalImg = document.getElementById('modalImage');
    const modalTitle = document.getElementById('modalTitle');
    const modalDate = document.getElementById('modalDate');
    const modalDesc = document.getElementById('modalDescription');
    const modalMeta = document.getElementById('modalMeta');
    const closeBtn = document.querySelector('.close');

    document.querySelectorAll('.gallery-item').forEach(item => {
        item.addEventListener('click', async function() {
            const id = this.dataset.id;
            try {
                const resp = await fetch(`/photo/${id}/`);
                const data = await resp.json();
                modalImg.src = data.image_url;
                modalTitle.textContent = data.title;
                modalDate.textContent = `${data.date}`;
                modalDesc.textContent = data.description;
                modalMeta.innerHTML = `Добавлено: ${data.created_at}`;
                modal.style.display = 'block';
                document.body.style.overflow = 'hidden';
            } catch(e) {
                console.error(e);
            }
        });
    });

    if (closeBtn) {
        closeBtn.onclick = () => {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        };
    }
    window.onclick = (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    };
});