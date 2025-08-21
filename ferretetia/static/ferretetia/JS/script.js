document.addEventListener('DOMContentLoaded', function () {
    var heroCarouselEl = document.querySelector('.hero-carousel.swiper');
    if (!heroCarouselEl || typeof Swiper === 'undefined') return;

    new Swiper(heroCarouselEl, {
        loop: true,
        autoplay: {
            delay: 4500,
            disableOnInteraction: false,
        },
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        slidesPerView: 1,
        effect: 'slide',
        speed: 700,
    });
});


