$(function(){

	//#region mobile-menu
    $('#menu').slicknav({
        label: 'منوی سایت',
        closedSymbol: "&#9664;",
        duration: 1000,
        easingOpen: "easeOutBounce",
        prependTo: '#demo2'
	});
	//#endregion
    
    //#region products-slick
	var $nav = $('.products-slick-nav').attr('data-nav');
	$('.products-slick').slick({

		rtl: true,
		slidesToShow: 4,
		slidesToScroll: 1,
		autoplay: true,
		infinite: true,
		speed: 300,
		pauseOnFocus:true,
		prevArrow:true,
		nextArrow:true,
		dots: false,
		arrows: true,
		appendArrows: $nav ? $nav : false,
		responsive: [{
		breakpoint: 991,
		settings: {
		  slidesToShow: 2,
		  slidesToScroll: 1,
		}
	  },
	  {
		breakpoint: 480,
		settings: {
		  slidesToShow: 1,
		  slidesToScroll: 1,
		}
	 },
	]
	});
    //#endregion
    
    //#region products-category-slick
	var $nav = $('.products-slick-nav').attr('data-nav');
	$('.products-category-slick').slick({

		rtl: true,
		slidesToShow: 3,
		slidesToScroll: 1,
		autoplay: true,
		infinite: true,
		speed: 300,
		pauseOnFocus:true,
		prevArrow:true,
		nextArrow:true,
		dots: false,
		arrows: true,
		appendArrows: $nav ? $nav : false,
		responsive: [{
		breakpoint: 991,
		settings: {
		  slidesToShow: 2,
		  slidesToScroll: 1,
		}
	  },
	  {
		breakpoint: 480,
		settings: {
		  slidesToShow: 1,
		  slidesToScroll: 1,
		}
	 },
	]
	});
	//#endregion

    //#region Price Slider
	$('.input-number').each(function() {
		var $this = $(this),
		$input = $this.find('input[type="number"]'),
		up = $this.find('.qty-up'),
		down = $this.find('.qty-down');

		down.on('click', function () {
			var value = parseInt($input.val()) - 1;
			value = value < 1 ? 1 : value;
			$input.val(value);
			$input.change();
			updatePriceSlider($this , value)
		})

		up.on('click', function () {
			var value = parseInt($input.val()) + 1;
			$input.val(value);
			$input.change();
			updatePriceSlider($this , value)
		})
	});

	var priceInputMax = document.getElementById('price-max'),
		priceInputMin = document.getElementById('price-min');

	priceInputMax.addEventListener('change', function(){
		updatePriceSlider($(this).parent() , this.value)
	});

	priceInputMin.addEventListener('change', function(){
		updatePriceSlider($(this).parent() , this.value)
	});

	function updatePriceSlider(elem , value) {
		if ( elem.hasClass('price-min') ) {
			console.log('min')
			priceSlider.noUiSlider.set([value, null]);
		} else if ( elem.hasClass('price-max')) {
			console.log('max')
			priceSlider.noUiSlider.set([null, value]);
		}
	}

	var priceSlider = document.getElementById('price-slider');
	if (priceSlider) {
		noUiSlider.create(priceSlider, {
			start: [1, 999],
			connect: true,
			step: 1,
			range: {
				'min': 1,
				'max': 999
			}
		});

		priceSlider.noUiSlider.on('update', function( values, handle ) {
			var value = values[handle];
			handle ? priceInputMax.value = value : priceInputMin.value = value
		});
	}

	//#endregion

});

function setCookie(name,value,days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "")  + expires + "; path=/";
}
function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)===' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}
function eraseCookie(name) {
    document.cookie = name +'=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}
function showMessage(message, type) {
	const msgDiv = document.createElement('div');
	msgDiv.className = `alert alert-${type} mt-2 msg-alert`;
	msgDiv.innerHTML = message;
	document.getElementById('message-container').appendChild(msgDiv);
}