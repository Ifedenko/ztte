const slider = document.getElementById('scrollSlider');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');

// Прокрутка на ширину видимой области (одного экрана слайдера)
function scrollNext() {
    const scrollAmount = slider.clientWidth;
    const maxScroll = slider.scrollWidth - slider.clientWidth;
    let newScrollLeft = slider.scrollLeft + scrollAmount;
    if (newScrollLeft > maxScroll) newScrollLeft = maxScroll;
    slider.scrollTo({ left: newScrollLeft, behavior: 'smooth' });
}

function scrollPrev() {
    const scrollAmount = slider.clientWidth;
    let newScrollLeft = slider.scrollLeft - scrollAmount;
    if (newScrollLeft < 0) newScrollLeft = 0;
    slider.scrollTo({ left: newScrollLeft, behavior: 'smooth' });
}

nextBtn.addEventListener('click', scrollNext);
prevBtn.addEventListener('click', scrollPrev);

// Доп. опция: блокировка кнопок в крайних положениях
function updateButtonsState() {
    const atStart = slider.scrollLeft <= 5;
    const atEnd = slider.scrollLeft + slider.clientWidth >= slider.scrollWidth - 5;
    prevBtn.disabled = atStart;
    nextBtn.disabled = atEnd;
    // Визуальное затенение для disabled
    prevBtn.style.opacity = atStart ? '0.5' : '1';
    nextBtn.style.opacity = atEnd ? '0.5' : '1';
}

slider.addEventListener('scroll', updateButtonsState);
window.addEventListener('resize', updateButtonsState);
updateButtonsState();
document.addEventListener('DOMContentLoaded', function() {

    const bookingForm = document.getElementById('excursionBookingForm');
    
    if (bookingForm) {
        bookingForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const formData = new FormData(bookingForm);
            const name = document.querySelector('input[placeholder="Иван Петров"]').value;
            const email = document.querySelector('input[type="email"]').value;
            const phone = document.querySelector('input[type="tel"]').value;
            const date = document.querySelector('input[type="date"]').value;
            const time = document.querySelector('select').value;
            const people = document.querySelector('input[type="number"]').value;
            const comments = document.querySelector('textarea').value;

            if (!name || !email || !phone || !date || !time) {
                alert('Пожалуйста, заполните все обязательные поля');
                return;
            }

            console.log('Заявка на экскурсию:', { name, email, phone, date, time, people, comments });

            alert('Спасибо! Ваша заявка отправлена. Мы свяжемся с вами для подтверждения в ближайшее время.');

            bookingForm.reset();
        });
    }
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    const dateInput = document.querySelector('input[type="date"]');
    if (dateInput) {
        const tomorrow = new Date();
        tomorrow.setDate(tomorrow.getDate() + 1);
        const year = tomorrow.getFullYear();
        const month = String(tomorrow.getMonth() + 1).padStart(2, '0');
        const day = String(tomorrow.getDate()).padStart(2, '0');
        dateInput.min = `${year}-${month}-${day}`;
    }
});
const eventModal = document.getElementById('eventModal');
const eventModalImage = document.getElementById('eventModalImage');
const eventModalTitle = document.getElementById('eventModalTitle');
const eventModalDate = document.getElementById('eventModalDate');
const eventModalDescription = document.getElementById('eventModalDescription');
const eventCloseBtn = eventModal.querySelector('.close');

document.querySelectorAll('.re_item').forEach(item => {
    item.addEventListener('click', function() {
        eventModalTitle.textContent = this.dataset.title;
        eventModalDescription.textContent = this.dataset.description;
        eventModalDate.textContent = this.dataset.date;
        eventModalImage.src = this.dataset.image;
        eventModal.style.display = 'block';
        document.body.style.overflow = 'hidden';
        });
    });

    eventCloseBtn.onclick = function() {
        eventModal.style.display = 'none';
        document.body.style.overflow = 'auto';
    };
    window.onclick = function(event) {
        if (event.target === eventModal) {
            eventModal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    };