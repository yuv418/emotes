class User < ApplicationRecord
  validates :username, presence: true, uniqueness: true
  has_many :api_keys, dependent: :destroy
  has_and_belongs_to_many :namespaces
end
