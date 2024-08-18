# default data

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manual_pages', '0003_faq'),
    ]

    operations = [
        migrations.RunSQL(
            "INSERT INTO  manual_pages_cleaningchecklistitem"
            "(item_text, is_visible, item_name, \"order\")"
            "VALUES ('Снимаем видео (дата, номер квартиры, количество комплектов белья, полотенец)', true, 'Снимаем видео (дата, номер квартиры, количество комплектов белья, полотенец)', 1)"
        ),
        migrations.RunSQL(
            "INSERT INTO  manual_pages_cleaningchecklistitem"
            "(item_text, is_visible, item_name, \"order\")"
            "VALUES ('Снимаем постельное белье с кровати, ставим быструю стирку', true, 'Снимаем постельное белье с кровати, ставим быструю стирку', 2)"
        ),
        migrations.RunSQL(
            "INSERT INTO  manual_pages_cleaningchecklistitem"
            "(item_text, is_visible, item_name, \"order\")"
            "VALUES ('Проверяем химию (Фейри, мыло, бумага, пакеты, порошок, чистин)', true, 'Проверяем химию (Фейри, мыло, бумага, пакеты, порошок, чистин)', 3)"
        ),
        migrations.RunSQL(
            "INSERT INTO  manual_pages_cleaningchecklistitem"
            "(item_text, is_visible, item_name, \"order\")"
            "VALUES ('Переходим на кухню, проверяем на работоспособность чайник, микроволновку', true, 'Переходим на кухню, проверяем на работоспособность чайник, микроволновку', 4)"
        ),
        migrations.RunSQL(
            "INSERT INTO  manual_pages_cleaningchecklistitem"
            "(item_text, is_visible, item_name, \"order\")"
            "VALUES ('Проверяем посуду (кружки, тарелки, стол. приборы, кастрюли, сковородки)', true, 'Проверяем посуду (кружки, тарелки, стол. приборы, кастрюли, сковородки)', 5)"
        ),
        migrations.RunSQL(
            "INSERT INTO  manual_pages_cleaningchecklistitem"
            "(item_text, is_visible, item_name, \"order\")"
            "VALUES ('Меняем мусорный пакет', true, 'Меняем мусорный пакет', 6)"
        ),
        migrations.RunSQL(
            "INSERT INTO  manual_pages_cleaningchecklistitem"
            "(item_text, is_visible, item_name, \"order\")"
            "VALUES ('Протираем кухонный гарнитур, холодильник', true, 'Протираем кухонный гарнитур, холодильник', 7)"
        ),
        migrations.RunSQL(
            "INSERT INTO  manual_pages_cleaningchecklistitem"
            "(item_text, is_visible, item_name, \"order\")"
            "VALUES ('Переходим в комнату, поднимаем матрас, проверяем целостность ламелей', true, 'Переходим в комнату, поднимаем матрас, проверяем целостность ламелей', 8)"
        ),
        migrations.RunSQL(
            "INSERT INTO  manual_pages_cleaningchecklistitem"
            "(item_text, is_visible, item_name, \"order\")"
            "VALUES ('Берем чистый комплект постельного, застилаем кровать', true, 'Берем чистый комплект постельного, застилаем кровать', 9)"
        ),
        migrations.RunSQL(
            "INSERT INTO  manual_pages_cleaningchecklistitem"
            "(item_text, is_visible, item_name, \"order\")"
            "VALUES ('Протираем все поверхности мебели', true, 'Протираем все поверхности мебели', 10)"
        ),
        migrations.RunSQL(
            "INSERT INTO  manual_pages_cleaningchecklistitem"
            "(item_text, is_visible, item_name, \"order\")"
            "VALUES ('Проверяем технику (утюг, фен, телевизор, кондиционер)', true, 'Проверяем технику (утюг, фен, телевизор, кондиционер)', 11)"
        ),
        migrations.RunSQL(
            "INSERT INTO  manual_pages_cleaningchecklistitem"
            "(item_text, is_visible, item_name, \"order\")"
            "VALUES ('В шкаф складываем комплекты постельного белья, одеяло‚ полотенце', true, 'В шкаф складываем комплекты постельного белья, одеяло‚ полотенце', 12)"
        ),
        migrations.RunSQL(
            "INSERT INTO  manual_pages_cleaningchecklistitem"
            "(item_text, is_visible, item_name, \"order\")"
            "VALUES ('Идем в ванную, складываем два полотенца на (стиральную машину или нишу)', true, 'Идем в ванную, складываем два полотенца на (стиральную машину или нишу)', 13)"
        ),
        migrations.RunSQL(
            "INSERT INTO  manual_pages_cleaningchecklistitem"
            "(item_text, is_visible, item_name, \"order\")"
            "VALUES ('Протираем и споласкиваем ванную (душевую кабину)', true, 'Протираем и споласкиваем ванную (душевую кабину)', 14)"
        ),
        migrations.RunSQL(
            "INSERT INTO  manual_pages_cleaningchecklistitem"
            "(item_text, is_visible, item_name, \"order\")"
            "VALUES ('Протираем унитаз, раковину, ниши, стир. машину', true, 'Протираем унитаз, раковину, ниши, стир. машину', 15)"
        ),
        migrations.RunSQL(
            "INSERT INTO  manual_pages_cleaningchecklistitem"
            "(item_text, is_visible, item_name, \"order\")"
            "VALUES ('Протираем зеркала от разводов (в начале мокрой тряпкой, затем сухой)', true, 'Протираем зеркала от разводов (в начале мокрой тряпкой, затем сухой)', 16)"
        ),
        migrations.RunSQL(
            "INSERT INTO  manual_pages_cleaningchecklistitem"
            "(item_text, is_visible, item_name, \"order\")"
            "VALUES ('Достаем постиранное белье, идем вешать на сушилку', true, 'Достаем постиранное белье, идем вешать на сушилку', 17)"
        ),
        migrations.RunSQL(
            "INSERT INTO  manual_pages_cleaningchecklistitem"
            "(item_text, is_visible, item_name, \"order\")"
            "VALUES ('Заканчиваем мытьем полов, складываем рабочий инвентарь на балкон', true, 'Заканчиваем мытьем полов, складываем рабочий инвентарь на балкон', 18)"
        ),
        migrations.RunSQL(
            "INSERT INTO  manual_pages_cleaningchecklistitem"
            "(item_text, is_visible, item_name, \"order\")"
            "VALUES ('Закрываем балкон, задвигаем занавески', true, 'Закрываем балкон, задвигаем занавески', 19)"
        ),
    ]
