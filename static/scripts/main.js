let selectedCity = undefined;

const cities = [
    ['Краснодар', '17'],
    ['Сочи', '27'],
    ['Ростов-на-Дону', '5'],
    ['Таганрог', '87']
];

const changeCity = city => {
    selectedCity = city[1];
    $('#citiesDropdown').html(city[0]);
}

const fillCities = () => {
    cities.forEach(city => {
        let city_verbouse_name = city[0];
        const cityTag = $(`<div class="dropdown-item city-dropdown-item">${city_verbouse_name}</div>`);
        cityTag.on('click', () => changeCity(city));
        $('#city-dropdown-menu').append(cityTag);
    });
}

$(document).ready(function () {
    fillCities();
    initOnClickEvents();
});

function renderGuests() {
    // const guestsDescription = `${document.getElementById('adult-guests').value} взрослых, ${document.getElementById('children').value} детей` + (document.getElementById('pets').checked ? ' с животными' : '');
    const guestsDescription = `${document.getElementById('adult-guests').value} взрослых, ${document.getElementById('children').value} детей`;
    $('#guests-dropdown').html(guestsDescription);
}

function initOnClickEvents() {
    $('#inc-adult-guests').on('click', () => document.getElementById('adult-guests').stepUp(1));
    $('#dec-adult-guests').on('click', () => document.getElementById('adult-guests').stepDown(1));
    $('#inc-children').on('click', () => document.getElementById('children').stepUp(1));
    $('#dec-children').on('click', () => document.getElementById('children').stepDown(1));
    $('#guests-submit').on('click', () => {
        renderGuests();
        const dropdown = bootstrap.Dropdown.getInstance(document.getElementById('guests-dropdown'));
        if (dropdown) {
            dropdown.hide();
        }
    });
}

function get_arrival_date() {
    let arrival_date = document.getElementById('arrival_date').value;

    if (arrival_date === 'Дата заезда') {
        return undefined
    }

    return arrival_date
}

function get_deportation_date() {
    let arrival_date = document.getElementById('deportation_date').value;

    if (arrival_date === 'Дата выезда') {
        return undefined
    }

    return arrival_date
}

function get_guests_count() {
    let guest_count = document.getElementById('adult-guests').value;

    return guest_count
}

function search_apartments() {
    let city = selectedCity;
    let arrival = get_arrival_date()
    let departure = get_deportation_date()
    let guests_counts = get_guests_count();
    let children_count = 1;
    // let with_pets = false;

    window.location = `appartments/list/?city=${city}&arrival=${arrival}&departure=${departure}&guests_counts=${guests_counts}`;
}

$(function () {
    $('input[name="arrival_date"]').daterangepicker({
        autoUpdateInput: false,
        locale: {
            applyLabel: "Сохранить",
            cancelLabel: 'Очистить',
            "daysOfWeek": [
                "Вс",
                "Пн",
                "Вт",
                "Ср",
                "Чт",
                "Пт",
                "Сб"
            ],
            "monthNames": [
                "Январь",
                "Февраль",
                "Март",
                "Апрель",
                "Май",
                "Июнь",
                "Июль",
                "Август",
                "Сентябрь",
                "Октябрь",
                "Ноябрь",
                "Декабрь"
            ],
            firstDay: 1
        },
        opens: 'right' // Открытие календаря слева от поля ввода
    });

    $('input[name="arrival_date"]').on('apply.daterangepicker', function (ev, picker) {
        $(this).val(picker.startDate.format('DD.MM.YYYY'));
        $('input[name="deportation_date"]').val(picker.endDate.format('DD.MM.YYYY'));
    });

    $('input[name="arrival_date"]').on('click', function () {
        $(this).data('daterangepicker').show();
    });

    $('input[name="deportation_date"]').on('click', function () {
        $('input[name="arrival_date"]').data('daterangepicker').show();
    });
});