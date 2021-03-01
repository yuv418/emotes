class AddKeyDigestToApiKeys < ActiveRecord::Migration[6.1]
  def change
    add_column :api_keys, :key_digest, :string
  end
end
