if [ -z "$TMUX" ]; then
	start=new-session
else
	start=new-window
fi

tmux $start \; \
  send-keys './scripts/dev-backend.sh' C-m \; \
  split-window -h \; \
  send-keys 'npm run watch' C-m \; 
