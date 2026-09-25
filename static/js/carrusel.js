/**
 * CARRUSEL DE FRUTAS CON PESTAÑAS - EL PASO FRUTERÍA (DISEÑO 4)
 */

document.addEventListener('DOMContentLoaded', () => {
    const track = document.getElementById('fruitCarouselTrack');
    const prevBtn = document.getElementById('carouselPrev');
    const nextBtn = document.getElementById('carouselNext');
    const tabs = document.querySelectorAll('.carousel-tab');
    const dotsContainer = document.getElementById('carouselDots');
    const cards = Array.from(track ? track.querySelectorAll('.carousel-card') : []);

    if (!track || cards.length === 0) return;

    let activeFilter = 'all';

    // Generar dots indicadores
    function updateDots() {
        if (!dotsContainer) return;
        dotsContainer.innerHTML = '';
        const visibleCards = cards.filter(c => !c.classList.contains('hidden-carousel-card'));
        const totalSlides = Math.ceil(visibleCards.length / getCardsPerView());

        for (let i = 0; i < totalSlides; i++) {
            const dot = document.createElement('button');
            dot.className = `carousel-dot ${i === 0 ? 'active' : ''}`;
            dot.setAttribute('aria-label', `Ir al slide ${i + 1}`);
            dot.addEventListener('click', () => {
                const cardWidth = visibleCards[0]?.offsetWidth || 280;
                const gap = 24;
                const scrollAmount = i * (cardWidth + gap) * getCardsPerView();
                track.scrollTo({ left: scrollAmount, behavior: 'smooth' });
                setActiveDot(i);
            });
            dotsContainer.appendChild(dot);
        }
    }

    function getCardsPerView() {
        const width = window.innerWidth;
        if (width < 640) return 1;
        if (width < 992) return 2;
        if (width < 1280) return 3;
        return 4;
    }

    function setActiveDot(index) {
        if (!dotsContainer) return;
        const dots = dotsContainer.querySelectorAll('.carousel-dot');
        dots.forEach((dot, idx) => {
            dot.classList.toggle('active', idx === index);
        });
    }

    // Scroll con botones
    function scrollCarousel(direction) {
        const visibleCards = cards.filter(c => !c.classList.contains('hidden-carousel-card'));
        if (visibleCards.length === 0) return;
        const cardWidth = visibleCards[0].offsetWidth;
        const gap = 24;
        const step = (cardWidth + gap) * Math.max(1, Math.floor(getCardsPerView() / 1.5));
        
        track.scrollBy({
            left: direction * step,
            behavior: 'smooth'
        });
    }

    if (prevBtn) {
        prevBtn.addEventListener('click', () => scrollCarousel(-1));
    }
    if (nextBtn) {
        nextBtn.addEventListener('click', () => scrollCarousel(1));
    }

    // Actualizar dots en scroll
    let scrollTimeout;
    track.addEventListener('scroll', () => {
        clearTimeout(scrollTimeout);
        scrollTimeout = setTimeout(() => {
            const visibleCards = cards.filter(c => !c.classList.contains('hidden-carousel-card'));
            if (visibleCards.length === 0) return;
            const cardWidth = visibleCards[0].offsetWidth;
            const gap = 24;
            const currentIndex = Math.round(track.scrollLeft / ((cardWidth + gap) * getCardsPerView()));
            setActiveDot(currentIndex);
        }, 100);
    });

    // Pestañas (Tabs)
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            activeFilter = tab.dataset.filter || 'all';

            // Animación suave de filtrado
            cards.forEach(card => {
                const cardCat = card.dataset.categoria;
                const match = activeFilter === 'all' || cardCat === activeFilter;
                
                if (match) {
                    card.classList.remove('hidden-carousel-card');
                    card.style.animation = 'fadeInUp 0.4s ease forwards';
                } else {
                    card.classList.add('hidden-carousel-card');
                }
            });

            // Resetear scroll
            track.scrollTo({ left: 0, behavior: 'smooth' });
            updateDots();
        });
    });

    // Inicializar
    updateDots();

    // Soporte para swipe/arrastrar en desktop y touch
    let isDown = false;
    let startX;
    let scrollLeft;

    track.addEventListener('mousedown', (e) => {
        isDown = true;
        track.classList.add('dragging');
        startX = e.pageX - track.offsetLeft;
        scrollLeft = track.scrollLeft;
    });

    track.addEventListener('mouseleave', () => {
        isDown = false;
        track.classList.remove('dragging');
    });

    track.addEventListener('mouseup', () => {
        isDown = false;
        track.classList.remove('dragging');
    });

    track.addEventListener('mousemove', (e) => {
        if (!isDown) return;
        e.preventDefault();
        const x = e.pageX - track.offsetLeft;
        const walk = (x - startX) * 1.5;
        track.scrollLeft = scrollLeft - walk;
    });

    // Toast de producto agregado
    const addBtns = document.querySelectorAll('.carousel-card .btn-add-fruit');
    addBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            const fruitName = btn.dataset.nombre || 'Fruta fresca';
            btn.classList.add('added');
            
            showToast(`🛒 "${fruitName}" agregado a tu lista de compra`);
            
            setTimeout(() => {
                btn.classList.remove('added');
            }, 1200);
        });
    });

    function showToast(message) {
        let toast = document.getElementById('fruitToast');
        if (!toast) {
            toast = document.createElement('div');
            toast.id = 'fruitToast';
            toast.className = 'fruit-toast';
            document.body.appendChild(toast);
        }
        toast.innerHTML = message;
        toast.classList.add('show');
        setTimeout(() => {
            toast.classList.remove('show');
        }, 2800);
    }

    window.addEventListener('resize', () => {
        updateDots();
    });
});
