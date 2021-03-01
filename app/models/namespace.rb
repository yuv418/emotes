class Namespace < ApplicationRecord
   has_and_belongs_to_many :user
   validates :slug, presence: true, uniqueness: true
end
