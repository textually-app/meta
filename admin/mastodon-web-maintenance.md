# Notes on administering a Mastodon server

The following notes show how to manage and keep up-to-date the
Mastodon (web) software on a Linux server after following the [initial
installation guide][mastodon-install].

## As the `mastodon` user

For most upgrade and maintenance tasks (besides actually restarting
the services) one needs to become the `mastodon` user. So, as a user
with superuser access, you need to switch first.

```
sudo su - mastodon
```

### Get to the default working directory

```
cd /home/mastodon/live
```

### Get latest source code

```
git pull
```

### Update Ruby environment

```
cd ~/.rbenv
git pull
cd ~/.rbenv/plugins/ruby-build
git pull
cd /home/mastodon/live
RUBY_CONFIGURE_OPTS=--with-jemalloc rbenv install 3.x.y
rbenv global 3.x.y
bundle install -j$(getconf _NPROCESSORS_ONLN)
```

### Migrate the database

```
RAILS_ENV=production bin/rails db:migrate
```

### Update the node environment

```
# bundle config deployment 'true'
# bundle config without 'development test'
yarn install --pure-lockfile
```

### Build static assets

```
RAILS_ENV=production bin/rails assets:precompile
```

## As root

Restarting the actual services requires `root` or a user with `sudo`
access.

### Restarting services

```
systemctl restart mastodon-sidekiq
systemctl restart mastodon-streaming <not needed generally>
systemctl restart mastodon-web
```

[mastodon-install]: https://docs.joinmastodon.org/admin/install/
