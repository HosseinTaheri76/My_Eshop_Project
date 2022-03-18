function get_query_params(checkboxes) {
    let category_id = document.getElementById('category_id');
    let query_string = `?${category_id.name}`;
    let attr_values = [];
    for (let checkbox of checkboxes) {
        if (checkbox.checked) {
            attr_values.push(`${checkbox.name}=on`);
        }
    }
    if (attr_values.length === 0) {
        return query_string
    }
    return query_string + '&' + attr_values.join('&');
}

function searchAjax(page=1) {
    const checkboxes = document.querySelectorAll('.filter-checkbox');
    const xhr = new XMLHttpRequest();
    xhr.open('GET', `/products/search/${get_query_params(checkboxes)}&page=${page}`);
    xhr.addEventListener('load', function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            let products = JSON.parse(xhr.responseText);
            build_products(products.results);
            if (products.results && get_query_params(checkboxes).split('&').length > 1){
            buildPagination(
                {
                    count : products.count,
                    next : products.next,
                    current : page,
                    previous : products.previous
                }
            )}
        }
    })
    xhr.send();
}
function buildPagination(params){
    let ul = document.getElementById('page-numlist');
    ul.innerHTML = '';
    for (let i=1 ; i <= Math.floor(params.count / 6) ; i++) {
        let li = document.createElement('li');
        li.innerHTML = `<a href="#" ${(params.current === i) ? 'class="page-active"' : ''}>${i}</a>`
        ul.appendChild(li);
        li.addEventListener('click', (e) =>{
            searchAjax(Number(e.target.innerHTML));
        })
    }
}

const search_form = document.getElementById('search-form');
if (search_form) {
    search_form.addEventListener('submit', function (e) {
        e.preventDefault();
        searchAjax();
    });
}


function build_products(products) {
    const products_container = document.querySelector('.products');
    products_container.innerHTML = '';
    let result = ''
    for (let product of products) {
        result += `
        <li class="box-product mt-2">
            <article>
                <img src="${product.image}" alt="" class="product-image">
                ${product.is_discounted ? `<span class="product-discount-badge">${product.discount_percent} % تخفیف</span>`: '' }
                <h2>
                    <a href="${product.url}">${product.title}</a>
                </h2>
                <h6><input type="checkbox" name="${product.id}:${product.root_category}"><label for=""> افزودن به لیست مقایسه </label></h6>
                <section class="detail">
                    <span class="price">${product.price} تومان</span>
                    <span class="basket"><i class="zmdi zmdi-shopping-basket"></i></span>
                    <section class="clearfix"></section>
                </section>
            </article>
        </li>
        `
        products_container.innerHTML = result;
    }
}

const compare_checkboxes = document.getElementsByClassName('compare-checkbox')

function handler(event) {
    let checkbox = event.target;
    if (checkbox.checked) {
        if (!getCookie('compare')) {
            setCookie('compare', checkbox.name, (1 / 48));
            create_compare_widget();
        } else {
            let current_value = getCookie('compare');
            if (current_value === '') {
                setCookie('compare', checkbox.name, (1 / 48));
                create_compare_widget();
            } else {
                let current_value_array = current_value.split(',');
                if (current_value_array.length === 4) {
                    alert('امکان مقایسه بیشتر از 4 محصول وجود ندارد');
                    return
                }
                if (current_value_array[0].split(':')[1] === checkbox.name.split(':')[1]) {
                    current_value_array.push(checkbox.name);
                    setCookie('compare', current_value_array.join(','), (1 / 48))
                    document.getElementById('compare-count').innerHTML = current_value_array.length.toString();

                } else {
                    checkbox.checked = false;
                    alert('شما نمی توانید محصولاتی که یک نوع نیستند را با هم مقایسه کنید')
                }
            }
        }
    } else {
        let products = getCookie('compare').split(',');
        let index = products.indexOf(checkbox.name);
        if (index !== -1) {
            products.splice(index, 1);
        }
        let new_value = products.join(',');
        setCookie('compare', new_value, (1 / 48));
        document.getElementById('compare-count').innerHTML = products.length.toString();
    }
}

function create_compare_widget() {
    const main_content = document.getElementById('main-content1');
    const compare = document.createElement('div');
    compare.innerHTML = `
            <a type="button" class="btn btn-info" href="/products/compare/">
                مقایسه <span class="badge" id="compare-count">1</span>
            </a>
            <button type="button" class="btn btn-danger" id="delete-compare"><i class="zmdi zmdi-delete"></i></button>
    `
    compare.className = 'btn-group compare-widget';
    compare.setAttribute('role', 'group');
    const products_content = document.getElementById('products-container');
    main_content.insertBefore(compare, products_content);
    const delete_compare = document.getElementById('delete-compare');
    if (delete_compare) {
        delete_compare.addEventListener('click', (e) => {
            for (let checkbox of document.getElementsByClassName('compare-checkbox')) {
                checkbox.checked = false;
            }
            eraseCookie('compare');
        })
    }
}

function deleteCompareWidget() {
    const main_content = document.getElementById('main-content1');
    const compare = document.querySelector('.compare-widget');
    main_content.removeChild(compare);
}

const compare_cookie = getCookie('compare');
for (let cmp_checkbox of compare_checkboxes) {
    cmp_checkbox.addEventListener('change', handler);
    if (compare_cookie && compare_cookie.split(',').includes(cmp_checkbox.name)) {
        cmp_checkbox.checked = true;
    }

}
var checkCookie = function () {
    var lastCookie = document.cookie; // 'static' memory between function calls
    return function () {
        var currentCookie = document.cookie;
        if (currentCookie !== lastCookie) {
            if (!getCookie('compare')) {
                deleteCompareWidget();
            }
            lastCookie = currentCookie; // store latest cookie

        }
    };
}();
document.addEventListener('DOMContentLoaded', () => {
    let compare = getCookie('compare');
    if (compare) {
        create_compare_widget();
        document.getElementById('compare-count').innerHTML = compare.split(',').length.toString();
    }
})
window.setInterval(checkCookie, 100); // run every 100 ms

