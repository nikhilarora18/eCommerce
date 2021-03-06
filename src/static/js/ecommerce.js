$(document).ready(function () {
    //contact form handler
    var contactForm = $(".contact-form")
    var contactFormMethod = contactForm.attr("method")
    var contactFormEndpoint = contactForm.attr("action")


    function displaySubmitting(submitBtn, defaultText, doSubmit) {
        if (doSubmit) {
            submitBtn.addClass("disabled")
            submitBtn.html("<i class='fa fa-spin fa-spinner'></i> Sending...")
        } else {
            submitBtn.removeClass("disabled")
            submitBtn.html(defaultText)
        }

    }

    contactForm.submit(function (event) {
        event.preventDefault()
        var contactFormSubmitBtn = contactForm.find("[type='submit']")
        var contactFormSubmitBtnTxt = contactFormSubmitBtn.text()

        var contactFormData = contactForm.serialize()
        var thisForm = $(this)
        displaySubmitting(contactFormSubmitBtn, "", true)
        $.ajax({
            method: contactFormMethod,
            url: contactFormEndpoint,
            data: contactFormData,
            success: function (data) {
                contactForm[0].reset();
                $.alert({
                    title: "Success",
                    content: data.message,
                    theme: "modern"
                })
                setTimeout(function () {
                    displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false)
                }, 500)

            },
            error: function (error) {
                var jsonData = error.responseJSON
                var msg = ""
                $.each(jsonData, function (key, value) { // key, value  array index / object
                    msg += key + ": " + value[0].message + "<br/>"
                })

                $.alert({
                    title: "Oops",
                    content: "An error occured",
                    theme: "modern"
                })
                setTimeout(function () {
                    displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false)
                }, 500)
            },

        })
    })

    //auto search
    var searchForm = $(".search-form");
    var searchInput = searchForm.find("[name='q']"); //input name=q
    var typingTimer;
    var typingInterval = 500; //1000=1sec
    var searchBtn = searchForm.find("[type='submit']");

    searchInput.keyup(function (event) {
        //key released
        clearTimeout(typingTimer);
        typingTimer = setTimeout(performSearch, typingInterval)
    });
    searchInput.keydown(function (event) {
        clearTimeout(typingTimer)
        //key pressed
    });

    function displaySearching() {
        searchBtn.addClass("disabled")
        searchBtn.html("<i class='fa fa-spin fa-spinner'></i>Searching...")
    }

    function performSearch() {
        displaySearching()
        var query = searchInput.val()
        setTimeout(function () {
            window.location.href = '/search/?q=' + query
        }, 500)

    }

    //cart stuff (product add and remove)
    var productForm = $(".form-product-ajax")
    productForm.submit(function (event) {
        event.preventDefault();
        var thisForm = $(this)
        //var actionEndpoint = thisForm.attr("action");
        var actionEndpoint = thisForm.attr("data-endpoint");
        var httpMethod = thisForm.attr("method");
        var formData = thisForm.serialize();
        $.ajax({
            url: actionEndpoint,
            method: httpMethod,
            data: formData,
            success: function (data) {
                var SubmitSpan = thisForm.find(".submit-span")
                if (data.added) {
                    SubmitSpan.html("In Cart <button type=\"submit\" class=\"btn btn-link\">Remove?</button>")
                }
                else {
                    SubmitSpan.html("<button type=\"submit\" class=\"btn btn-success\">Add in Cart</button>")
                }
                var navbarCount = $(".navbar-cart-count")
                navbarCount.text("(" + data.cartItemCount + ")")
                var currentPath = window.location.href
                if (currentPath.indexOf("cart") != -1) {
                    refreshCart()
                }
            },
            error: function (errorData) {
                //console.log("error")
                $.alert({
                    title: "Oops",
                    content: "An error occured",
                    theme: "modern"
                })
            },
        })
    })

    function refreshCart() {
        var cartTable = $(".cart-table")
        var cartBody = cartTable.find(".cart-body")
        var productRows = cartBody.find(".cart-product")
        var currentUrl = window.location.href

        var refreshCartUrl = 'api/cart/';
        var refreshCartMethod = "GET";
        var data = {};
         console.log("ajax reached")
        $.ajax({
            url: refreshCartUrl,
            method: refreshCartMethod,
            data: data,
            success: function (data) {
                console.log("sucess")
                if (data.products.length > 0) {
                    console.log("success ajax")
                    var hiddenCartItemRemoveForm = $(".cart-item-remove-form")
                    productRows.html("")
                    var i = data.products.length
                    $.each(data.products, function (index, value) {
                        var newCartItemRemove = hiddenCartItemRemoveForm.clone()
                        newCartItemRemove.css("display", "block")
                        newCartItemRemove.find(".cart-item-product-id").val(value.id)
                        cartBody.prepend("<tr><th scope\"row\">" + i + "</th><td><a href='" + value.url + "'>" + value.name + "</a>" + newCartItemRemove.html() + "</td><td>" + value.price + "</td></tr>")
                        i--
                    })
                    cartBody.find(".cart-subtotal").text(data.subtotal)
                    cartBody.find(".cart-total").text(data.total)
                }
                else {
                    console.log("refreshed")
                    window.location.href = currentUrl
                }
            },
            error: function (errorData) {
                $.alert({
                    title: "Oops",
                    content: "An error occured",
                    theme: "modern",
                })
                //console.log("error")
            }
        })

    }
})