$(function () {

    // =================================
    // Tooltip
    // =================================
    var tooltipTriggerList = [].slice.call(
        document.querySelectorAll('[data-bs-toggle="tooltip"]')
    );
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // fixed header

    $(window).scroll(function () {
        if ($(window).scrollTop() >= 60) {
            $('header').addClass('fixed-header');
        } else {
            $('header').removeClass('fixed-header');
        }
    });

    // scroll

    $(".scroll-link").on("click", function (t) {
        var o = $(this);
        $("html, body").stop().animate({
            scrollTop: $(o.attr("href")).offset().top - 10
        }, 1e3), t.preventDefault()
    })

    // Aos

    AOS.init({
        once: true,
    });


    // Review Slider

    $('.review-slider .owl-carousel').owlCarousel({
        loop: true,
        items: 1,
        margin: 0,
        dots: true,
        nav: true,
        navText: ["<i class='ti ti-arrow-left'></i>", "<i class='ti ti-arrow-right'></i>"],
        autoplay: true,
        autoplayTimeout: 5000,
        autoplayHoverPause: true,
    })


});

//add Shadow to header on scroll
document.addEventListener("DOMContentLoaded", function () {
    document.addEventListener("scroll", function () {
        if (document.body.scrollTop > 60 || document.documentElement.scrollTop > 60) {
            document.querySelector(".top-header").classList.add("shadow-sm");  
            document.querySelector(".top-header").classList.add("bg-white"); 
        } else {
            document.querySelector(".top-header").classList.remove("shadow-sm");
            document.querySelector(".top-header").classList.remove("bg-white");
        }
    })
});