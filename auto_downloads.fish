#!/usr/bin/env fish

set OK 1
set FAIL 0

function dl_from_github_repo 
	set rel_info_json (curl -s "https://api.github.com/repos/$argv[1]/releases/latest")
	if test (string length "$rel_info_json") -eq 0
		echo "Error: Could not get release info"
		return $FAIL
	end 
	set dl_assets (echo $rel_info_json | jq -r ".assets")
	set kws	(string split " " $argv[3])
	for kw in $kws 
		set dl_assets (echo $dl_assets | jq -r "map(select(.name | contains(\"$kw\")) | .)")
		echo $dl_assets " satisify " $kw
		if test (string length "$dl_assets") -eq 0
			echo "Error: Could not find given download from release info"
			return $FAIL
		end
	end
	set dl_assets $dl_assets 
	echo $dl_assets "dl_assets"
	set num_of_dl_assets (echo $dl_assets | jq length)
	echo $num_of_dl_assets
	if test $num_of_dl_assets -ne 1
		echo "Error: Many assets are satisified"
		for idx in (seq 0 (math $num_of_dl_assets - 1))
			echo (echo $dl_assets | jq -r ".[$idx] | .name")
		end
		return $FAIL
	end
	set dl_url (echo $dl_assets | jq -r ".[0] | .browser_download_url")
	echo $dl_url
	wget $dl_url
	return $OK
end
# bat 
dl_from_github_repo sharkdp/bat tar "linux"
