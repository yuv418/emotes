class RemoveKeyFromApiKey < ActiveRecord::Migration[6.1]
  def change
    remove_column :api_keys, :key, :string
  end
end
