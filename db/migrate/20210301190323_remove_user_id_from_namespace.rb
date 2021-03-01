class RemoveUserIdFromNamespace < ActiveRecord::Migration[6.1]
  def change
    remove_column :namespaces, :user_id, :integer
  end
end
