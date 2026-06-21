document.addEventListener('DOMContentLoaded', function () {

    const images = document.querySelectorAll('.main-img');

    images.forEach(img => {
        img.addEventListener('load', function () {
            this.classList.add('loaded');
            const container = this.closest('.blur-container');
            if (container) {
                container.style.filter = 'none';
                container.style.transform = 'scale(1)';
            }
        });

        if (img.complete) {
            img.classList.add('loaded');
            const container = img.closest('.blur-container');
            if (container) {
                container.style.filter = 'none';
                container.style.transform = 'scale(1)';
            }
        }
    });

    const filterBtns = document.querySelectorAll('.filter-btn');

    filterBtns.forEach(btn => {
        btn.addEventListener('click', function () {
            filterBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');

            const filter = this.dataset.filter;
            const params = new URLSearchParams(window.location.search);
            params.set('filter', filter);

            const yearSelect = document.getElementById('yearSelect');
            const monthSelect = document.getElementById('monthSelect');

            if (yearSelect && yearSelect.value) params.set('year', yearSelect.value);
            if (monthSelect && monthSelect.value) params.set('month', monthSelect.value);

            window.location.href = `${window.location.pathname}?${params.toString()}`;
        });
    });

    const yearSelect = document.getElementById('yearSelect');

    if (yearSelect) {
        yearSelect.addEventListener('change', function () {
            const params = new URLSearchParams(window.location.search);

            if (this.value) params.set('year', this.value);
            else params.delete('year');

            window.location.href = `${window.location.pathname}?${params.toString()}`;
        });
    }

    const monthSelect = document.getElementById('monthSelect');

    if (monthSelect) {
        monthSelect.addEventListener('change', function () {
            const params = new URLSearchParams(window.location.search);

            if (this.value) params.set('month', this.value);
            else params.delete('month');

            window.location.href = `${window.location.pathname}?${params.toString()}`;
        });
    }

    const modal = document.getElementById('modal');
    const modalImg = document.getElementById('modalImage');
    const modalTitle = document.getElementById('modalTitle');
    const modalDate = document.getElementById('modalDate');
    const modalDesc = document.getElementById('modalDescription');
    const modalMeta = document.getElementById('modalMeta');
    const closeBtn = document.querySelector('.close');

    document.querySelectorAll('.gallery-item').forEach(item => {
        item.addEventListener('click', async function () {
            const id = this.dataset.id;

            try {
                const resp = await fetch(`/photo/${id}/`);
                const data = await resp.json();

                modalImg.src = data.image_url;
                modalTitle.textContent = data.title;
                modalDate.textContent = data.date;
                modalDesc.textContent = data.description;
                modalMeta.textContent = `Добавлено: ${data.created_at}`;

                modal.style.display = 'block';
                document.body.style.overflow = 'hidden';
            } catch (e) {
                console.error(e);
            }
        });
    });

    if (closeBtn) {
        closeBtn.addEventListener('click', function () {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        });
    }

    window.addEventListener('click', function (e) {
        if (e.target === modal) {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    });

});