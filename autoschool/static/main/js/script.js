// Инициализация после загрузки DOM
document.addEventListener('DOMContentLoaded', function() {
    // начало js карусели мейна
    const carousel = document.querySelector('.carousel');
    if (carousel) {
        const group = carousel.querySelector('.group');
        if (group) {
            // получаем ширину блока и карусели
            const groupWidth = group.offsetWidth;
            const carouselWidth = carousel.offsetWidth;

            // считаем, сколько блоков нужно добавить
            const blocksNeeded = Math.ceil(carouselWidth / groupWidth) + 1;

            for (let i = 0; i < blocksNeeded; i++) {
                const clone = group.cloneNode(true);
                clone.setAttribute('aria-hidden', 'true');
                carousel.appendChild(clone);
            }
        }
    }
    // конец js карусели мейна

    // начало js комментариев - инициализация всех слайдеров на странице
    const swiperContainers = document.querySelectorAll('.card-wrapper');
    
    swiperContainers.forEach(function(container) {
        new Swiper(container, {
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
    });
    // конец js комментариев
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