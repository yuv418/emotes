class AddAdminUserToUsers < ActiveRecord::Migration[6.1]
  def change
    admin = User.create(username: "Admin", admin: true)
    key = admin.api_keys.create

    puts "ADMIN API KEY (SAVE THIS VALUE): #{key.jwt}"
  end
end
