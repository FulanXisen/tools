# (wsl only) set proxy using default clash port
function set_proxy
    set -xg hostip (cat /etc/resolv.conf | grep nameserver | awk '{ print $2 }')
    set -xg https_proxy "http://$hostip:7890"
    set -xg http_proxy "http://$hostip:7890"
    printf 'https proxy = %s\nhttp  proxy = %s\n' "$https_proxy" "$http_proxy"
end

function unset_proxy
    set -e https_proxy
    set -e http_proxy
    printf 'https proxy = %s\nhttp  proxy = %s\n' "$https_proxy" "$http_proxy"
end
