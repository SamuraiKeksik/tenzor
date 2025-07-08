#!/bin/bash

services=$(systemctl list-units -a --no-legend 'foobar-*' | awk '{print $1}')
echo "Найденные сервисы: "
echo "$services"

for service in $services; do
  echo "Работа с сервисом $service"
  serviceWorkingDir=$(systemctl show -p WorkingDirectory $service)
  serviceExecStart=$(systemctl show -p ExecStart $service)
  serviceName=$(echo "$service" | sed 's/.service//')

  echo "serviceWorkingDir = $serviceWorkingDir"
  echo "serviceExecStart = $serviceExecStart"
  echo "serviceName = $serviceName"

  if [ -z "$serviceWorkingDir" ] || [ -z "$serviceExecStart" ] || [ -z "$serviceName" ]; then
    echo "Не удалось поулчить параметры для $service"
    continue
  fi

  systemctl stop $service
  mkdir -p "/srv/data/$serviceName"
  if [ $? -ne 0 ]; then
    echo "Ошибка остановки $service - " >&2
    exit 1
  fi
  echo "Создана новая директория для $service"


  cp -r "/opt/misc/$serviceName" "/srv/data/"
  if [ $? -ne 0 ]; then
    echo "Ошибка копирования директории /opt/misc/$serviceName в /srv/data - " >&2
    exit 1
  fi
  echo "Директория /opt/misc/$serviceName/ скопирована в /srv/data/$serviceName/"

  sed -i "s|$serviceWorkingDir|WorkingDirectory=/srv/data/$serviceName|" "/etc/systemd/system/$service"
  sed -ir "s|ExecStart=/opt/misc/|ExecStart=/srv/data/|" "/etc/systemd/system/$service"
  if [ $? -ne 0 ]; then
    echo "Ошибка изменения WorkingDirectory или ExecStart - " >&2
    exit 1
  fi
   echo "WorkingDirectory и ExecStart изменены"

  systemctl daemon-reload
  systemctl start $service
  if [ $? -ne 0 ]; then
    echo "Ошибка запуска $service - " >&2
    exit 1
  fi

  echo "Сервис $service успешно обновлен"
done