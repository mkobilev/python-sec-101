Жил-да-был разработчик, который любил XML. Любил настолько, что даже знал, как задавать `ENTITY`, чтобы потом переиспользовать их:
```
<!--?xml version="1.0" ?-->
<!DOCTYPE userCard [
                    <!ENTITY firstName "{firstName}">
                    <!ENTITY lastName "{lastName}">
                    <!ENTITY days "{days}">
                    ]>
<userInfo>
	<FIO>&firstName; &lastName;</FIO>
	<firstName>&firstName;</firstName>
	<lastName>&lastName;</lastName>
	<workDays>&days;</workDays>
    <totalSalary>TODO</totalSalary>
</userInfo>
```
Казалось бы, как это поможет прочитать файл `/app/flag.txt`?
