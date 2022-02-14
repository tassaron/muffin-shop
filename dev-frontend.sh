if [ -z "$TMUX" ]; then
	start=new-session
else
	start=new-window
fi

tmux $start \; \
  send-keys './dev-backend.sh' C-m \; \
  split-window -h \; \
  send-keys 'cd tassaron_flask/nodejs && npm run watch' C-m \; 
