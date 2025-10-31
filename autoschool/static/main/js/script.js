// Инициализация после загрузки DOM
document.addEventListener('DOMContentLoaded', function() {
    // Нативная ленивая загрузка картинок (для всех, где не задано иначе)
    document.querySelectorAll('img:not([loading])').forEach(function(img){
        img.setAttribute('loading', 'lazy');
    });
    document.querySelectorAll('img:not([decoding])').forEach(function(img){
        img.setAttribute('decoding', 'async');
    });

    // Ленивая подстановка background-image для секций с .lazy-bg
    (function initLazyBackgrounds(){
        var items = Array.prototype.slice.call(document.querySelectorAll('.lazy-bg'));
        if (!items.length) return;

        function applyBg(el){
            var src = el.getAttribute('data-bg');
            if (!src) return;
            var grad = el.getAttribute('data-bg-gradient');
            el.style.backgroundImage = grad ? (grad + ', url("' + src + '")') : 'url("' + src + '")';
            el.classList.remove('lazy-bg');
        }

        if ('IntersectionObserver' in window) {
            var io = new IntersectionObserver(function(entries){
                entries.forEach(function(entry){
                    if (entry.isIntersecting) {
                        applyBg(entry.target);
                        io.unobserve(entry.target);
                    }
                });
            }, { rootMargin: '200px 0px' });
            items.forEach(function(el){ io.observe(el); });
        } else {
            // Fallback: подставить после полной загрузки
            window.addEventListener('load', function(){ items.forEach(applyBg); });
        }
    })();

    // Инициализация карусели мейна после полной загрузки ресурсов
    function initCarousel() {
        const carousel = document.querySelector('.carousel');
        if (!carousel) return;

        // Удаляем ранее созданные клоны
        carousel.querySelectorAll('.group[aria-hidden="true"]').forEach(function(n){ n.remove(); });

        const group = carousel.querySelector('.group');
        if (!group) return;

        // Используем размеры после загрузки изображений
        const groupWidth = group.scrollWidth || group.offsetWidth;
        const carouselWidth = carousel.clientWidth || carousel.offsetWidth;
        if (!groupWidth || !carouselWidth) return;

        const blocksNeeded = Math.ceil(carouselWidth / groupWidth) + 1;
        for (let i = 0; i < blocksNeeded; i++) {
            const clone = group.cloneNode(true);
            clone.setAttribute('aria-hidden', 'true');
            carousel.appendChild(clone);
        }
    }

    // Debounce helper для resize
    function debounce(fn, wait){
        let t; return function(){
            clearTimeout(t); t = setTimeout(fn, wait);
        };
    }

    window.addEventListener('load', initCarousel);
    window.addEventListener('resize', debounce(initCarousel, 200));

    // начало js комментариев - инициализация всех слайдеров на странице
    const swiperContainers = document.querySelectorAll('.card-wrapper');
    
    swiperContainers.forEach(function(container) {
        const swiper = new Swiper(container, {
            loop: true,
            spaceBetween: 30,

            // Pagination bullets
            pagination: {
                el: container.querySelector('.swiper-pagination'),
                clickable: true,
                dynamicBullets: true,
            },

            // Navigation arrows
            navigation: {
                nextEl: container.querySelector('.swiper-button-next'),
                prevEl: container.querySelector('.swiper-button-prev'),
            },

            // Responsive breakpoints
            breakpoints: container.closest('.about-fourth-block') ? {
                0: {
                    slidesPerView: 1
                }
            } : {
                0: {
                    slidesPerView: 1
                },
                1100: {
                    slidesPerView: 2
                },
                1900: {
                    slidesPerView: 3
                },
            }
        });

        // Добавляем обработчики клика на картинки в блоке изображений
        const imageBlocks = container.querySelectorAll('.cv-second-block-images-block');
        
        // Функция обновления курсоров и стилей для картинок
        function updateImageCursors() {
            const activeIndex = swiper.realIndex; // Получаем реальный индекс активного слайда
            imageBlocks.forEach(function(imageBlock) {
                const images = imageBlock.querySelectorAll('img');
                images.forEach(function(img, index) {
                    if (index === activeIndex) {
                        img.style.cursor = 'default'; // Обычный курсор для активной картинки
                        img.classList.add('active-image'); // Добавляем класс активной картинки
                    } else {
                        img.style.cursor = 'pointer'; // Курсор-указатель для неактивных
                        img.classList.remove('active-image'); // Убираем класс активной картинки
                    }
                });
            });
        }
        
        // Инициализируем курсоры при загрузке
        updateImageCursors();
        
        // Обновляем курсоры при смене слайда
        swiper.on('slideChange', function() {
            updateImageCursors();
        });
        
        imageBlocks.forEach(function(imageBlock) {
            const images = imageBlock.querySelectorAll('img');
            images.forEach(function(img, index) {
                img.addEventListener('click', function() {
                    // Переключаемся на слайд с соответствующим индексом
                    // Так как loop: true, используем slideToLoop для корректного переключения
                    swiper.slideToLoop(index);
                });
            });
        });
    });
    // конец js комментариев

    // --- Booking page helpers ---
    const lessonTypeSelect = document.getElementById('lesson_type');
    const lessonTypeWrapper = document.getElementById('lesson-type-item');

    function openSelect(selectEl) {
        if (!selectEl) return;
        // Try to open native dropdown programmatically
        selectEl.focus();
        try { selectEl.click(); } catch (e) {}
    }

    if (lessonTypeWrapper && lessonTypeSelect) {
        // Clicking anywhere in the wrapper (except on the select itself) opens dropdown
        lessonTypeWrapper.addEventListener('click', function(e) {
            if (e.target && e.target.tagName.toLowerCase() === 'select') return;
            openSelect(lessonTypeSelect);
        });
    }

        // --- Contact page: copy phone numbers ---
        document.querySelectorAll('.contact-copy-btn').forEach(function(btn){
            btn.addEventListener('click', function(e){
                e.preventDefault();
                var container = btn.closest('.contact-number');
                var p = container ? container.querySelector('p') : null;
                var text = p ? (p.textContent || '').trim() : '';
                if (!text) return;
                if (navigator.clipboard && navigator.clipboard.writeText) {
                    navigator.clipboard.writeText(text);
                } else {
                    var ta = document.createElement('textarea');
                    ta.value = text;
                    ta.style.position = 'fixed';
                    ta.style.top = '-1000px';
                    document.body.appendChild(ta);
                    ta.focus();
                    ta.select();
                    document.execCommand('copy');
                    document.body.removeChild(ta);
                }
            });
        });
});

// Language changer: compute new next URL with language prefix and submit
// Exposed globally so existing inline onchange can call it
window.changeLanguage = function (select) {
try {
    var form = select.form;
    var selected = select.value;
    var nextInput = document.getElementById('language-next');
    var path = window.location.pathname || '/';

    // Pattern: path starts with '/xx' or '/xxx' where xx/xxx is language prefix
    var langPrefixPattern = /^\/[A-Za-z]{2,3}(?:\/|$)/;
    var newPath;

    if (path === '/') {
    newPath = '/' + selected + '/';
    } else if (langPrefixPattern.test(path)) {
    newPath = path.replace(/^\/[A-Za-z]{2,3}/, '/' + selected);
    } else {
    newPath = '/' + selected + path;
    }

    // preserve query string and hash
    newPath += window.location.search + window.location.hash;

    if (nextInput) nextInput.value = newPath;
    form.submit();
} catch (e) {
    // fallback
    if (select && select.form) select.form.submit();
}
};

window.LogoRedirect = function() {
    window.location.href = '/';
}