upload:
	rsync -av -e ssh --exclude=".git" ../ComfyS3Plus	flux:/home/ubuntu/ComfyUI-audio/custom_nodes