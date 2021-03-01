class AddUserToApiKeys < ActiveRecord::Migration[6.1]
  def change
    add_reference :api_keys, :user, null: false, foreign_key: true
  end
end
