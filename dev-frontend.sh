tmux new-session \; \
  send-keys './dev-backend.sh' C-m \; \
  split-window -h \; \
  send-keys 'cd tassaron_flask/nodejs && npm run watch' C-m \; 
