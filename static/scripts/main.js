let selectedCity = undefined;

const cities = [
    'Краснодар',
    'Сочи',
    'Ростов-на-Дону',
    'Таганрог'
];

const changeCity = city => {
    selectedCity = city;
    $('#citiesDropdown').html(city);
}

const fillCities = () => {
    cities.forEach(city => {
        const cityTag = $(`<div class="dropdown-item city-dropdown-item">${city}</div>`);
        cityTag.on('click', () => changeCity(city));
        $('#city-dropdown-menu').append(cityTag);
    });
}

$(document).ready(function() {
    fillCities();
    initOnClickEvents();
});

function renderGuests() {
    const guestsDescription = `${document.getElementById('adult-guests').value} взрослых, ${document.getElementById('children').value} детей` + (document.getElementById('pets').checked ? ' с животными' : '');
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