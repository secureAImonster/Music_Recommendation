#Prefy
spotifyからユーザの気分に合わせたレコメンドシステムの開発

##DB設計
###table一覧
####users
- _id  Number
- name String
- mail_address {type: String, required: true, unique: true}
- password {type: String, required: true }

####songs
- _id Number
- user {type: Number, ref: 'User' }
- genre String
- playtimes Number (再生回数)

####histories
- _id Number
- song {type: Number, ref: 'Song'}
- temp Number
- weather Number
- time String (年、月、日)
- date String (日時分秒)

####feedbacks
- _id Number
- song {type: Number, ref: 'Song'}
- status Number (feedback)
- playtimes Number (再生回数)

####機械学習のための形式
machine_learning/csv/(user_id).csv

### migration
insert
```
$ cd ~/prefy/migrations
$ node insert
```

remove
```
$ cd ~/prefy/migrations
$ node remove-all
```
